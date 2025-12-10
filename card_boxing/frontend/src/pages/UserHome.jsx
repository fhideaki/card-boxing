import "../styles/login.css"; // mantém o estilo CRT que você já tem

export default function UserHome() {
  return (
    <div className="container">
      <h1>Menu do Jogador</h1>

      <div className="buttons">
        <button>Meus Robôs</button>
        <button>Loja de Peças</button>
        <button>Batalhar</button>
        <button>Logout</button>
      </div>
    </div>
  );
}