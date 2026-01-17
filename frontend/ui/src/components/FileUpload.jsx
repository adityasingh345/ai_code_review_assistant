export default function FileUpload({ onAnalyze, loading }) {

  const handleSubmit = (e) => {
    e.preventDefault(); // ✅ FIXED
    const file = e.target.file.files[0];
    if (!file) return;
    onAnalyze(file);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="file"
        name="file"
        accept=".py, .js, .ts, .java, .zip"
        disabled={loading}
      />

      <br /><br />

      <button type="submit" disabled={loading}>
        {loading ? "Analyzing..." : "Analyze Code"}
      </button>
    </form>
  );
}
