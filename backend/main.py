from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Form
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from schemas import codeReviewresponse, GithubRepoRequest, GitHubPRReviewRequest
from ai_review import review_code
from utils import extract_code_files

from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from database import Base, engine
from auth_routes import router as auth_router
from models import CodeReview
import json
import re
from database import get_db
from github_utils import fetch_repo_files
from github_pr_utils import fetch_pr_files


SECRET_KEY = "ADITYA"
ALGORITHM = "HS256"

app = FastAPI(title="AI code Review Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        email = payload.get("sub")
        if email is None:
            raise Exception()
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/review", )
async def review_code_api(
    file: UploadFile=File(...),
    language: str = Form("python"), 
    current_user: str = Depends(get_current_user),
    db: Session =Depends(get_db)):
    
    print(" ENTERED /review endpoint")

    
    content = await file.read()
    
    if file.filename.endswith(".zip"):
        extracted_files = extract_code_files(content)

        results = {}
        total_issues = 0

        for filename, code in extracted_files.items():
            ai_result = review_code(code, language)
            issues = ai_result.get("issues", [])
            results[filename] = issues
            total_issues += len(issues)
        
        db_review = CodeReview(
            user_email= current_user,
            file_name = file.filename,
            review_type = "zip",
            result_json = json.dumps({"files": results})
        )
        db.add(db_review)
        db.commit()

        return {
            "type": "project",
            "user": current_user,
            "summary": {
                "total_files": len(results),
                "total_issues": total_issues
            },
            "files": results
        }

    
    code_text = content.decode("utf-8")
    
    ai_result = review_code(code_text, language)

    db_review = CodeReview(
        user_email=current_user,
        file_name=file.filename,
        review_type="single",
        result_json=json.dumps(ai_result)
    )
    db.add(db_review)
    db.commit()
    
    return {
        "type": "single",
        "user": current_user,
        "language": language,
        "issues": ai_result.get("issues", []) 
    }
    
#get history review
@app.get("/history")
def get_review_history(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    reviews = (
        db.query(CodeReview).filter(CodeReview.user_email == current_user).order_by(CodeReview.created_at.desc()).all()
    )
    
    return [
        {
            "id": r.id,
            "file_name": r.file_name,
            "review_type": r.review_type,
            "created_at": r.created_at
        }
        for r in reviews
    ]
    
@app.post("/review/github")
def review_github_repo(
    payload: GithubRepoRequest,
    github_token: str | None = None,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    repo_url = payload.repo_url
    github_token = payload.github_token
    
    try:
        owner, repo = repo_url.replace("https://github.com/", "").split("/")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid GitHub URL")

    files = fetch_repo_files(owner, repo, github_token)

    results = {}
    for filename, code in files.items():
        print("reviewing files",filename)
        ai_result = review_code(code, "python")
        results[filename] = ai_result.get("issues", [])

    # Save to DB
    db_review = CodeReview(
        user_email=current_user,
        file_name=repo,
        review_type="github",
        result_json=json.dumps(results)
    )
    db.add(db_review)
    db.commit()

    return {
        "type": "github",
        "repo": repo,
        "total_files": len(results),
        "files": results
    }

# delete specific history
@app.delete("/history/{review_id}")
def delete_review(
    review_id: int,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    review = db.query(CodeReview).filter(
        CodeReview.id == review_id,
        CodeReview.user_email == current_user
    ).first()

    if not review:
        raise HTTPException(status_code=404, detail="Review Not found")
    
    db.delete(review)
    db.commit()

@app.delete("/history")
def delete_all(
    current_user: str = Depends(get_current_user),
    db : Session = Depends(get_db)
):
    db.query(CodeReview).filter(
        CodeReview.user_email == current_user
    ).delete()

    db.commit()

    return {"message: all history deleted"}


def parse_pr_url(pr_url: str):
    match = re.match(
        r"https://github\.com/([^/]+)/([^/]+)/pull/(\d+)",
        pr_url
    )
    if not match:
        return None
    return match.group(1), match.group(2), int(match.group(3))


@app.post("/review/github/pr")
def review_pull_request(
    payload: GitHubPRReviewRequest,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    pr_url = payload.pr_url
    github_token = payload.github_token 
    parsed = parse_pr_url(pr_url)
    if not parsed:
        raise HTTPException(status_code=400, detail="Invalid PR URL")
    
    owner, repo, pr_number = parsed

    files = fetch_pr_files(owner=owner, repo=repo, pr_number=pr_number, token=github_token)

    results = {}

    for filename, content in files.items():

        patch = content.get("patch", "no diff available")
        ai_result = review_code(
           f"""
        Review this GitHub Pull Request change carefully.

        DIFF:
        {patch}

        FULL FILE:
        {content['code']}
        """,
            "go"            
        )
        results[filename] = ai_result.get("issues", [])

    db_review = CodeReview(
        user_email=current_user,
        file_name=f"{repo} PR #{pr_number}",
        review_type="github_pr",
        result_json=json.dumps(results)
    )
    db.add(db_review)
    db.commit()

    return {
        "type": "github_pr",
        "repo": repo,
        "pr_number": pr_number,
        "total_files": len(results),
        "files": results
    }