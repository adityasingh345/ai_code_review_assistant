const BASE_URL = "http://127.0.0.1:8000";

export async function signup(email, password){
    const res = await fetch(`${BASE_URL}/auth/signup`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({email, password})
    });

    if (!res.ok) throw new Error("signup failed");
    return res.json()
}


export async function login(email, password){
    const res = await fetch(`${BASE_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({email, password})
    });
    if (!res.ok) throw new Error("login failed");
    return res.json()
}

export async function get_history(token){
    const res = await fetch(`${BASE_URL}/history`, {
        method: "GET",
        headers: {
            Authorization: `Bearer ${token}`
        }
    });

    if (!res.ok) throw new Error("failed to fetch history");
    return res.json()
}

export async function analyzefile(file, token, language = "python") {

    const formData = new FormData();
    formData.append("file", file);
    formData.append("language", language)

    // send request to backend
    const response = await fetch(`${BASE_URL}/review`, {
        method : "POST",
        headers: {
            Authorization: `Bearer ${token}`
        },
        body: formData
        });

    if (!response.ok) {
        throw new Error("analysis failed");
    }

    return response.json();
    
}

export async function analyzegithubrepo(repourl, githubtoken, token){
    const res = await fetch(`${BASE_URL}/review/github`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({
      repo_url: repourl,
      github_token: githubtoken
    })
  });

  if (!res.ok) throw new Error("GitHub review failed");
  return res.json();
}