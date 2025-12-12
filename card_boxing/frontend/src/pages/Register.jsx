import { useState } from "react";
import { useNavigate } from "react-router-dom";
// Importe seu arquivo de estilos se for o mesmo do login ou crie um novo
// import "../styles/login.css"; 


export default function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  async function handleRegister(e) {
    e.preventDefault();

    // 1. Validação simples no lado do cliente
    if (password !== confirmPassword) {
      setMessage("Erro: A senha e a confirmação de senha não coincidem.");
      return;
    }

    setMessage("Aguardando...");

    try {
      // 2. Chama a rota de Registro do seu backend Flask (http://127.0.0.1:5000/api/register)
      const response = await fetch("http://127.0.0.1:5000/api/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        // Envia o username e password no corpo da requisição
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();
      setMessage(data.message);

      // 3. Se o registro for bem-sucedido (status 201), redireciona para a tela de login
      if (response.status === 201) {
        // Redireciona de volta para a tela de login para o usuário entrar
        navigate("/"); 
      }
    } catch (error) {
      setMessage("Erro ao conectar ao servidor de registro.");
    }
  }

  // Função para voltar para a tela de Login
  function handleGoToLogin() {
    navigate("/");
  }

  return (
    <div className="container">
      <h1>Card Boxing - Registro</h1>

      <form onSubmit={handleRegister}>
        <label>Novo Usuário</label>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />

        <label>Senha</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        
        <label>Confirme a Senha</label>
        <input
          type="password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          required
        />

        <div className="buttons">
          <button type="submit">Finalizar Registro</button>
          {/* Botão para voltar à tela de login */}
          <button type="button" onClick={handleGoToLogin}>
            Voltar para Login
          </button>
        </div>
      </form>

      {/* Mensagem da API/Validação */}
      <p style={{ marginTop: "20px" }}>{message}</p>
    </div>
  );
}