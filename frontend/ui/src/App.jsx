import { useState } from "react";
import { analyzefile, get_history, analyzegithubrepo} from "./api";
import FileUpload from "./components/FileUpload";
import ReviewResult from "./components/ReviewResult";
import Login from "./Login";
import Signup from "./Signup";


function App() {
  const [history, SetHistory] = useState([]);
  const [showHistory, setShowHistory] = useState(false);
  const [showSignup, setShowSignup] = useState(false);
  const [Token, SetToken] = useState(null);
  const [result, SetResult] = useState(null);
  const [loading, SetLoading] = useState(false)

  const [repoUrl, setRepoUrl] = useState("");
  const [githubToken, setGithubToken] = useState("");


  async function handleAnalyze(file) {
    SetLoading(true);
    SetResult(null); // clear old results

    try {
      const data = await analyzefile(file, Token);
      SetResult(data);
      setShowHistory(false) 
    } catch (err) {
      alert("Error analyzing code");
    } finally {
      SetLoading(false);
    }
  }

  async function handleGetHistory() {
  try {
    const data = await get_history(Token);
    SetHistory(data);
    setShowHistory(true);
    SetResult(null); //hide current result
    } catch {
      alert("Failed to load history");
    }
  }

  //auth gate
  if (!Token) {
    return showSignup ? (
      <Signup onSwitch={() => setShowSignup(false)} />
    ) : (
      <Login
        onLogin={SetToken}
        onSwitch={() => setShowSignup(true)}
      />
    );
  }  




  //main app
  return (
    <div style={{ padding: "20px" }}>
      <h1>AI Code Review Assistant</h1>

      <FileUpload onAnalyze={handleAnalyze} loading={loading} />

      <h3>Review GitHub Repository</h3>

      <input
        placeholder="https://github.com/owner/repo"
        value={repoUrl}
        onChange={(e) => setRepoUrl(e.target.value)}
      />

      <br />

      <input
        placeholder="GitHub Token (optional)"
        value={githubToken}
        onChange={(e) => setGithubToken(e.target.value)}
      />

      <br />

      <button
        onClick={async () => {
            try {
              SetLoading(true);
              setShowHistory(false);

              const data = await  analyzegithubrepo(repoUrl, githubToken, Token);
              SetResult(data);
            } catch (err) {
              console.error(err);
              alert("GitHub analysis failed");
            } finally {
              SetLoading(false);
            }
          }}
      >
        Analyze GitHub Repo
      </button>


      {loading && <p>Analyzing code...</p>}

      {!showHistory && <ReviewResult result={result} />}

      {showHistory && (
        <div>
          <h3>Review History</h3>
          {history.length === 0 && <p>No past reviews</p>}
          {history.map((h) => (
            <div key={h.id} style={{ border: "1px solid #ddd", margin: "8px", padding: "8px" }}>
              <p><strong>{h.file_name}</strong> ({h.review_type})</p>
              <small>{new Date(h.created_at).toLocaleString()}</small>
            </div>
          ))}
        </div>
      )}

      <br />
      <button onClick={handleGetHistory}>Get History</button>
      <button onClick={() => SetToken(null)}>Logout</button>
    </div>
  );
}

export default App;
