import { useState } from "react";
import { signup } from "./api";

export default function Signup({ onSwitch }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  async function handleSignup(e) {
    e.preventDefault();
    try {
      await signup(email, password);
      alert("Signup successful. Please login.");
      onSwitch();
    } catch {
      alert("Signup failed");
    }
  }

  return (
    <form onSubmit={handleSignup}>
      <h2>Signup</h2>

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

      <button type="submit">Signup</button>
      <p onClick={onSwitch} style={{ cursor: "pointer" }}>
        Already have an account? Login
      </p>
    </form>
  );
}
