import "../styles/login.css";
import { useNavigate } from "react-router-dom";

export default function UserHome() {
  const navigate = useNavigate();
  
  return (
    <div className="menu">
      <button onClick={() => navigate("/robots")}>Meus Robôs</button>
      <button>Loja de Peças</button>
      <button>Batalhar</button>
      <button onClick={() => navigate("/")}>Logout</button>
    </div>
  );
}