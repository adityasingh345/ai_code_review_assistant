# structured output 
# we will define structure of how the input should be there and output should be there

from pydantic import BaseModel
from typing import List, Optional

# with schema you know exactly what data looks like 

#one problem in the code 
class codeIssue(BaseModel):
    # what kind of issue 
    issue_type: str
    # how serious it 
    severity: str
    #where it occurs
    line_number: Optional[int]
    #human readable reason
    explanation: str
    # suggest fix
    improved_code: Optional[str]
    
#this is what api returns to frontend 
class codeReviewresponse(BaseModel):
    language: str
    issues: List[codeIssue]
    
class GithubRepoRequest(BaseModel):
    repo_url: str
    github_token: Optional[str] = None

class GitHubPRReviewRequest(BaseModel):
    pr_url: str
    github_token: Optional[str] = None
