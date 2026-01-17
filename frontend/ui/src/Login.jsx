import { useState } from "react";
import { login } from "./api";

export default function Login({ onLogin, onSwitch }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  async function handleLogin(e) {
    e.preventDefault();
    try {
      const data = await login(email, password);
      onLogin(data.access_token);
    } catch {
      alert("Login failed");
    }
  }

  return (
    <form onSubmit={handleLogin}>
      <h2>Login</h2>

      <input
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      /><br />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      /><br /><br />

      <button type="submit">Login</button>
      <p onClick={onSwitch} style={{ cursor: "pointer" }}>
        No account? Signup
      </p>
    </form>
  );
}
