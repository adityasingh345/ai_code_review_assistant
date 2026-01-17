export default function ReviewResult({ result }) {
  if (!result) return null;

  if (result.type === "github") {
    return (
      <div>

        {Object.entries(result.files).map(([filename, issues]) => (
          <div key={filename}>
            <h4>{filename}</h4>
            {issues.length === 0 && <p>No issues 🎉</p>}
            {issues.map((issue, idx) => (
              <p key={idx}>
                <strong>{issue.issue_type}</strong> ({issue.severity}) — {issue.explanation}
              </p>
            ))}
          </div>
        ))}
      </div>
    );
  }


  // single file result
  if (result.type == "single"){
    return (
      <div>
        <h3>Language: {result.language}</h3>

        {result.issues.map((issue, index) => (
          <div key={index}>
            <p><strong>{issue.issue_type}</strong> ({issue.severity})</p>
            <p>{issue.explanation}</p>
          </div>
        ))}
      </div>
    );
  }
  // ZIP/project result
  return (
     <div>
      <h2>Project Review Summary</h2>
      <p>Total Files: {result.summary.total_files}</p>
      <p>Total Issues: {result.summary.total_issues}</p>

      {Object.entries(result.files).map(([filename, issues]) => (
        <div key={filename} style={{ marginTop: "20px" }}>
          <h4>{filename}</h4>

          {issues.length === 0 && <p>No issues 🎉</p>}

          {issues.map((issue, idx) => (
            <div key={idx}>
              <p><strong>{issue.issue_type}</strong> ({issue.severity})</p>
              <p>{issue.explanation}</p>
            </div>
          ))}
        </div>
      ))}
    </div>
  );
}
