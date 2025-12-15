import { useEffect, useState } from "react";
import "../styles/teste.css";

export default function Teste() {
  const [attackArchetype, setAttackArchetype] = useState(null);

  useEffect(() => {
    fetch("http://localhost:5000/api/archetypes/atk/preview")
      .then((res) => res.json())
      .then((data) => {
        console.log("DADOS RECEBIDOS:", data);
        setAttackArchetype(data); // confirme se é atk mesmo
      })
      .catch((err) =>
        console.error("Erro ao buscar arquétipo de ataque:", err)
      );
  }, []);

  if (!attackArchetype) {
    return <p>Carregando...</p>;
  }

    const radarStats = {
    ...attackArchetype.base_stats,
    ...attackArchetype.secondary_stats
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

          return (
            <text
              key={attr.key}
              x={center + (radius + 20) * Math.cos(rad)}
              y={center + (radius + 20) * Math.sin(rad)}
              textAnchor="middle"
              dominantBaseline="middle"
              className="radar-label"
            >
              {attr.label}
            </text>
          );
        })}
      </svg>
    );
  }

  // 🔹 RETURN FINAL — UM ÚNICO PAI
  return (
    <div className="page-wrapper">
      {/* Página A4 da imagem */}
      <div className="a4-container">
        <img
          src={`/images/${attackArchetype.image}`}
          alt={attackArchetype.label}
          className="a4-image"
        />
      </div>

      {/* Página A4 do radar */}
      <div className="a4-container">
        {renderRadarChart(radarStats)}
      </div>
    </div>
  );
}
