import requests 
import base64

ALLOWED_EXTENSIONS = (".py", ".js", ".ts", ".java")

def fetch_repo_files(owner, repo, token=None):
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"
        
    url = f"https://api.github.com/repos/{owner}/{repo}/contents"
    
    response = requests.get(url, headers=headers)
    
    response.raise_for_status()
    
    files ={}
    
    for item in response.json():
        if item["type"] == "file" and item["name"].endswith(ALLOWED_EXTENSIONS):
            file_res = requests.get(item["download_url"], headers=headers)
            files[item["path"]] = file_res.text
            
    return files    