import { useState } from "react";

export default function CreateRobot() {
  const [name, setName] = useState("");
  const [selected, setSelected] = useState(null);

  const archetypes = {
    ATK: {
      label: "Ataque (ATK)",
      image: "/images/atk.png", // coloque qualquer imagem temporária
      cards: ["Golpe Pesado", "Rajada", "Destruição"],
      stats: { atk: 9, def: 3, spd: 7 },
    },
    DEF: {
      label: "Defesa (DEF)",
      image: "/images/def.png",
      cards: ["Fortaleza", "Guardião", "Barreira"],
      stats: { atk: 4, def: 10, spd: 3 },
    },
    BAL: {
      label: "Balanceado (BAL)",
      image: "/images/bal.png",
      cards: ["Fluir", "Adaptar", "Resposta"],
      stats: { atk: 6, def: 6, spd: 6 },
    },
  };

  return (
    <div className="min-h-screen bg-black text-white flex items-center justify-center p-10">
      
      <div className="w-[900px] bg-neutral-900 rounded-2xl p-8 shadow-xl">

        {/* TÍTULO */}
        <h1 className="text-3xl mb-6 text-center font-bold">
          Criar Novo Robô
        </h1>

        {/* NOME */}
        <label className="block mb-4">
          <span className="text-lg">Nome do Robô:</span>
          <input
            type="text"
            className="mt-2 w-full p-3 rounded-lg bg-neutral-800 border border-neutral-700 focus:ring focus:ring-green-500"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </label>

        {/* SELEÇÃO DE ARQUÉTIPO */}
        <h2 className="text-xl mt-8 mb-4 font-semibold">Selecione o Arquétipo:</h2>

        <div className="grid grid-cols-3 gap-6">
          {Object.entries(archetypes).map(([key, data]) => (
            <div
              key={key}
              onClick={() => setSelected(key)}
              className={`cursor-pointer rounded-2xl p-4 bg-neutral-800 border-2 transition 
              ${selected === key ? "border-green-400" : "border-transparent"} hover:border-green-600`}
            >
              <img src={data.image} className="h-48 w-full object-contain mb-4" />
              <h3 className="text-xl text-center font-bold">{data.label}</h3>
            </div>
          ))}
        </div>

        {/* INFO DO ARQUÉTIPO ESCOLHIDO */}
        {selected && (
          <div className="mt-10 p-6 bg-neutral-800 rounded-xl border border-neutral-700">

            <h3 className="text-2xl mb-4 font-bold">
              Arquétipo Selecionado: {archetypes[selected].label}
            </h3>

            {/* CARTAS */}
            <p className="text-lg mb-3 font-semibold">Cartas Iniciais:</p>
            <ul className="ml-4 list-disc mb-6">
              {archetypes[selected].cards.map((c) => (
                <li key={c}>{c}</li>
              ))}
            </ul>

            {/* GRÁFICO DE STATS (barras horizontais) */}
            <p className="text-lg font-semibold mb-4">Distribuição de Stats:</p>

            {Object.entries(archetypes[selected].stats).map(([stat, value]) => (
              <div key={stat} className="mb-3">
                <p className="uppercase text-sm mb-1">{stat}</p>
                <div className="w-full bg-neutral-700 rounded-full h-3">
                  <div
                    className="bg-green-500 h-3 rounded-full"
                    style={{ width: `${value * 10}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        )}

        {/* BOTÕES */}
        <div className="flex justify-between mt-10">
          <button
            className="px-8 py-3 rounded-xl bg-neutral-700 hover:bg-neutral-600 transition"
            onClick={() => (window.location.href = "/userhome")}
          >
            Voltar
          </button>

          <button
            className="px-8 py-3 rounded-xl bg-green-600 hover:bg-green-500 transition font-bold"
            onClick={() => alert("Robô criado (mock)!")}
          >
            Criar Robô
          </button>
        </div>

      </div>
    </div>
  );
}
