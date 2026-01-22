import requests

allowed_extension = (".py", ".js", ".ts", "java", ".go")

def fetch_pr_files(owner , repo, pr_number , token =None):
    headers = {}
    if token :
        headers["Authorization"] = f"token {token}"

    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"

    response = requests.get(url, headers=headers)

    response.raise_for_status()

    files = {}

    for item in response.json():
        if item["filename"].endswith(allowed_extension):
            raw_url = item["raw_url"]
            file_res = requests.get(raw_url, headers=headers)
            files[item["filename"]] = {
                "code": file_res.text,
                "patch": item.get("patch", "")
            }

    return files