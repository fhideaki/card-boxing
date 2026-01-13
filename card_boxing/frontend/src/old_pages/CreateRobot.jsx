import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/createrobot.css";

export default function Teste() {
  const navigate = useNavigate();
  
  const [archetypes, setArchetypes] = useState([]);

  const [selectedName, setSelectedName] = useState("Nenhum");
  const [selectedArchetype, setSelectedArchetype] = useState(null);

  const [robotName, setRobotName] = useState("");

  useEffect(() => {
    fetch("http://localhost:5000/api/archetypes/all/preview") 
      .then((res) => res.json())
      .then((data) => {
        console.log("LISTA RECEBIDA:", data);
        // data aqui deve ser um array: [{...atk}, {...def}, {...bal}]
        setArchetypes(data); 
      })
      .catch((err) => console.error("Erro ao buscar arquétipos:", err));
}, []);

  const handleSelectArchetype = (archetype) => {
    setSelectedName(archetype.label);
    setSelectedArchetype(archetype);
  };

  const handleConfirmar = async () => {
    if (!robotName || !selectedArchetype) {
      alert("Por favor, digite um nome e selecione um arquétipo!");
      return;
    }

  const playerId = localStorage.getItem("playerId");

  const payload = {
    robot_name: robotName,
    player_id: playerId,
    archetype_key: selectedArchetype.key
  };

  try {
    const response = await fetch("http://localhost:5000/api/robots/create", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (response.ok) {
      alert("Robô construído com sucesso!");
      navigate("/robots");
    } else {
      const errorData = await response.json();
      alert("Erro: " + errorData.message);
    }
  } catch (err) {
    console.error("Erro na requisição:", err);
  }
};

  // 🔹 Radar criado dentro do próprio componente
  function renderRadarChart(stats) {
    const size = 220;
    const center = size / 2;
    const radius = 80;

    const attributes = [
    { key: "constitution", label: "CON", angle: -90 },
    { key: "strength",     label: "STR", angle: -30 },
    { key: "agility",      label: "AGI", angle: 30 },
    { key: "attack",       label: "ATK", angle: 90 },
    { key: "defense",      label: "DEF", angle: 150 },
    { key: "clinch",       label: "CLI", angle: -150 },
    ];

    const maxValue = Math.max(...Object.values(stats));

    const basePolygon = attributes.map(attr => {
        const rad = (attr.angle * Math.PI) / 180;
        return `${center + radius * Math.cos(rad)},${center + radius * Math.sin(rad)}`;
    });

    const statPolygon = attributes.map(attr => {
        const rad = (attr.angle * Math.PI) / 180;
        const value = Math.min(stats[attr.key] / maxValue, 1);
        return `${center + radius * value * Math.cos(rad)},${center + radius * value * Math.sin(rad)}`;
    });

    return (
      <svg
        className="radar-chart"
        width={size}
        height={size}
      >
        <polygon
          className="radar-grid"
          points={basePolygon.join(" ")}
        />

        <polygon
          className="radar-stats"
          points={statPolygon.join(" ")}
        />

        {attributes.map((attr) => {
          const rad = (attr.angle * Math.PI) / 180;

          const labelX = center + (radius + 20) * Math.cos(rad);
          const labelY = center + (radius + 20) * Math.sin(rad);
          
          return (
            <text key={attr.key} x={labelX} y={labelY} textAnchor="middle" dominantBaseline="middle" className="radar-label">
              {attr.label}
            </text>
          );
        })}
      </svg>
    );
  }
          // const valueX = center + (radius + 36) * Math.cos(rad);
          // const valueY = center + (radius + 36) * Math.sin(rad);

  if (archetypes.length === 0) return <p>Carregando arquétipos...</p>;

  return (
    <div className="main-page-container">
      <div className="cards-grid-container">
        {archetypes.map((archetype, index) => {
        const radarStats = {
          ...archetype.base_stats,
          ...archetype.secondary_stats
        };
        return (
          <div key={index} className="page-wrapper clickable-card" onClick={() => handleSelectArchetype(archetype)}>
            {/* Página A4 da imagem */}
            <div className="a4-container a4-image-container">
              <img
                src={`/images/${archetype.image}`}
                alt={archetype.label}
                className="a4-image"
              />
              <h2 className="archetype-title">{archetype.label}</h2>
            </div>

            {/* Página A4 do radar */}
            <div className="a4-container a4-info-container">
              {renderRadarChart(radarStats)}

              <div className="status-box">
                <h3>HP: {archetype.base_stats.HP}</h3>
              </div>

              <div className="deck-box">
                <h3>Deck Base</h3>
                <ul>
                  {archetype.deck.base_cards.map(card => (
                    <li key={card.id}>{card.name} x{card.quantity}</li>
                  ))}
                </ul>

                <h3>Cartas Especiais</h3>
                
                <ul>
                  {archetype.deck.special_cards.map(card => (
                    <li key={card.id}>{card.name} x{card.quantity}</li>
                  ))}
                </ul>

              </div>
            </div>
          </div>
        );
        })} 
      </div>

      <div className="selection-display">
        <h2>Arquétipo Selecionado: <span>{selectedName}</span></h2>
      </div>     
      <div className="input-group">
        <label htmlFor="robot-name">Nome do seu Robô:</label>
        <input 
          id="robot-name"
          type="text" 
          placeholder="Digite o nome..." 
          value={robotName} 
          onChange={(e) => setRobotName(e.target.value)} // Atualiza o estado ao digitar
        />
        <button 
          className="confirm-button" 
          onClick={handleConfirmar}
          disabled={!robotName || !selectedArchetype} // Desabilita se estiver incompleto
        >
          FINALIZAR CONSTRUÇÃO
      </button>
      </div>
    </div>
  );
}
