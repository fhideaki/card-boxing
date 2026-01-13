import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/userhome.css";

export default function MyRobots() {
  const navigate = useNavigate();
  const [robots, setRobots] = useState([]);

  useEffect(() => {
    async function fetchRobots() {
      const userId = localStorage.getItem("playerId")
      if (!userId) return;

      try {
        const response = await fetch(`http://127.0.0.1:5000/api/my_robots?user_id=${userId}`);
        const data = await response.json();
        setRobots(data.robots);
      } catch (error) {
        console.log("Erro ao carregar robôs", error);
      }
    }
    fetchRobots();
  }, []);

  return (
    <div className="robot-page">
      
      {/* Painel esquerdo */}
      <div className="side-menu">
        <button className="btn" onClick={() => navigate("/create-robot")}>
          Criar Novo Robô
        </button>

        <button className="btn secondary" onClick={() => navigate("/home")}>
          Voltar
        </button>
      </div>

      {/* Lista de robôs */}
      <div className="robot-list">
        {robots.length === 0 ? (
          <p>Você ainda não criou nenhum robô.</p>
        ) : (
          robots.map((robot) => (
            <RobotCard key={robot.id} robot={robot} />
          ))
        )}
      </div>
    </div>
  );
}

function RobotCard({ robot }) {
  return (
    <div className="robot-card">
      <h2>{robot.name}</h2>

      {/* Área exibida somente no HOVER */}
      <div className="robot-details">
        <div className="parts-grid">
          {robot.parts.map((part) => (
            <img
              key={part.id}
              src={`/icons/${part.icon}`}
              alt={part.part_name}
              className="part-icon"
            />
          ))}
        </div>

        {/* Gráfico de status */}
        <div className="stats-chart">
          {/* Você futuramente substitui por radar chart */}
          <pre>{JSON.stringify(robot.stats, null, 2)}</pre>
        </div>
      </div>
    </div>
  );
}
