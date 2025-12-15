import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/createrobot.css";

export default function CreateRobot() {
  // ================================
  // ESTADOS (dados que mudam na tela)
  // ================================
  const [name, setName] = useState("");
  const [selected, setSelected] = useState(null);
  const [archetypes, setArchetypes] = useState(null);

  const navigate = useNavigate();

  // ================================
  // BUSCA DOS ARQUÉTIPOS (API)
  // ================================
  useEffect(() => {
    fetch("http://localhost:5000/api/archetypes")
      .then((res) => res.json())
      .then((data) => setArchetypes(data))
      .catch((err) =>
        console.error("Erro ao buscar arquétipos:", err)
      );
  }, []);

  // ================================
  // FUNÇÃO DE CÁLCULO (igual ao Python)
  // ================================
  const calculateStats = (base) => {
    const defense = base.constitution + 0.6 * base.strength;
    const attack = base.strength + 0.6 * base.agility;
    const clinch = base.agility + 0.6 * base.strength;

    return { ...base, defense, attack, clinch };
  };

  // ================================
  // LOADING (antes da API responder)
  // ================================
  if (!archetypes) {
    return (
      <div className="min-h-screen bg-black text-white flex items-center justify-center">
        <p>Carregando arquétipos...</p>
      </div>
    );
  }

  // ================================
  // RENDER
  // ================================
  return (
    <div className="min-h-screen bg-black text-white flex flex-col items-center p-4 md:p-10">
      <div className="w-full max-w-[900px] bg-neutral-900 rounded-2xl p-8 shadow-xl my-10">
        <h1 className="text-3xl mb-6 text-center font-bold">
          Criar Novo Robô
        </h1>

        {/* NOME */}
        <label className="block mb-4">
          <span className="text-lg">Nome do Robô:</span>
          <input
            type="text"
            className="mt-2 w-full p-3 rounded-lg bg-neutral-800 border border-neutral-700"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </label>

        <h2 className="text-xl mt-8 mb-4 font-semibold">
          Selecione o Arquétipo:
        </h2>

        {/* LISTA DE ARQUÉTIPOS */}
        <div className="grid grid-cols-3 gap-6 w-full">
          {Object.entries(archetypes).map(([key, data]) => (
            <div
              key={key}
              onClick={() => setSelected(key)}
              className={`cursor-pointer rounded-2xl p-6 bg-neutral-800 border-2 transition-all ${
                selected === key
                  ? "border-green-400 bg-neutral-700"
                  : "border-transparent"
              }`}
            >
              {/* IMAGEM DO ARQUÉTIPO */}
              <div className="w-full h-32 flex items-center justify-center mb-4">
                <img
                  src={`/images/${data.image}`}
                  alt={data.label}
                  className="max-h-full max-w-full object-contain"
                />
              </div>

              <h3 className="text-xl text-center font-bold">
                {data.label}
              </h3>
            </div>
          ))}
        </div>

        {/* DETALHES DO ARQUÉTIPO */}
        {selected && (
          <div className="mt-10 p-6 bg-neutral-800 rounded-xl border border-neutral-700">
            <h3 className="text-2xl mb-4 font-bold">
              Arquétipo Selecionado: {archetypes[selected].label}
            </h3>

            {/* STATS */}
            <p className="text-lg font-semibold mb-4">
              Distribuição de Stats:
            </p>

            {(() => {
              const stats = calculateStats(
                archetypes[selected].base_stats
              );

              const statsToDisplay = [
                { key: "constitution", label: "Constituição" },
                { key: "strength", label: "Força" },
                { key: "agility", label: "Agilidade" },
                { key: "HP", label: "HP" },
                { key: "attack", label: "Ataque" },
                { key: "defense", label: "Defesa" },
                { key: "clinch", label: "Clinch" },
              ];

              const maxValue = Math.max(
                ...statsToDisplay.map((s) => stats[s.key])
              );

              return statsToDisplay.map((stat) => (
                <div key={stat.key} className="mb-4">
                  <p className="uppercase text-sm mb-1">
                    {stat.label}
                  </p>
                  <div className="w-full bg-neutral-700 rounded-full h-3">
                    <div
                      className="bg-green-500 h-3 rounded-full"
                      style={{
                        width: `${
                          (stats[stat.key] / maxValue) * 100
                        }%`,
                      }}
                    />
                  </div>
                  <p className="text-xs opacity-70 mt-1">
                    Valor: {stats[stat.key].toFixed(1)}
                  </p>
                </div>
              ));
            })()}
          </div>
        )}

        {/* BOTÕES */}
        <div className="flex justify-between mt-10">
          <button
            className="px-8 py-3 rounded-xl bg-neutral-700"
            onClick={() => navigate("/userhome")}
          >
            Voltar
          </button>

          <button
            className="px-8 py-3 rounded-xl bg-green-600 font-bold"
            onClick={() => {
              console.log("Robô criado:", { name, selected });
              navigate("/userhome");
            }}
          >
            Criar Robô
          </button>
        </div>
      </div>
    </div>
  );
}
