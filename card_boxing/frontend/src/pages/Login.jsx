import { useState } from "react";
import "../styles/login.css";
import { useNavigate } from "react-router-dom";


export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const navigate = useNavigate();


  async function handleLogin(e) {
    e.preventDefault();
    setMessage("Aguardando...");

    try {
      const response = await fetch("http://127.0.0.1:5000/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();
      setMessage(data.message);

     if (response.status === 200) {
      navigate("/home");  // ⬅ Redireciona para UserHome
    }
  } catch (error) {
    setMessage("Erro ao conectar ao servidor.");
  }
}

  return (
    <div className="container">
      <h1>Card Boxing</h1>

      <form onSubmit={handleLogin}>
        <label>Usuário</label>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />

        <label>Senha</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <div className="buttons">
          <button type="submit">Entrar</button>
        </div>
      </form>

      {/* Mensagem da API */}
      <p style={{ marginTop: "20px" }}>{message}</p>
    </div>
  );
}
