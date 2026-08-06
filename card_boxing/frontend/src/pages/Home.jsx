import React, { useState } from "react";

export default function Home() {
    // 1 - Estados para armazenar o que o usuário selecionou
    const [rounds, setRounds] = useState(1);
    const [oponente, setOponente] = useState("");
    const [roboSelecionado, setRoboSelecionado] = useState("");
    const [deckSelecionado, setDeckSelecionado] = useState("");

    // 2 - Dados simulados que virão do Backend futuramente
    const amigosOnline = ["É o Ferpas", "Wollt", "KusukiOficial", "Daniel da Bahia", "Colantuomo"];
    const meusRobos = ["Metabee", "Megatron"];
    const decksDoRobo = {
        "Metabee": ["Deck1", "Deck2"],
        "Megatron": ["Deck3", "Deck4"]
    };

    const podeLutar = roboSelecionado && deckSelecionado && oponente;

    const selectClasses =
        "w-full appearance-none rounded-lg border border-slate-700 bg-slate-800/80 px-4 py-2.5 text-slate-100 " +
        "shadow-sm transition focus:border-red-500 focus:outline-none focus:ring-2 focus:ring-red-500/40 " +
        "disabled:cursor-not-allowed disabled:opacity-40";

    return (
        <div className="flex min-h-[calc(100vh-4rem)] items-center justify-center bg-slate-950 px-4 py-10">
            <main className="w-full max-w-lg rounded-2xl border border-slate-800 bg-slate-900/60 p-8 shadow-2xl shadow-black/40 backdrop-blur">
                <div className="mb-8 text-center">
                    <h1 className="text-2xl font-bold tracking-tight text-white">Preparar Luta</h1>
                    <p className="mt-1 text-sm text-slate-400">Configure a partida antes de entrar no ringue</p>
                </div>

                <div className="space-y-5">
                    {/* Lista 1 - Quantidade de Rounds */}
                    <div>
                        <label className="mb-1.5 block text-sm font-medium text-slate-300">
                            Quantidade de Rounds
                        </label>
                        <select
                            className={selectClasses}
                            value={rounds}
                            onChange={(e) => setRounds(e.target.value)}
                        >
                            {[1, 3, 5, 7, 9].map(num => (
                                <option key={num} value={num}>{num}</option>
                            ))}
                        </select>
                    </div>

                    {/* Lista 2 - Oponente (Amigos Online) */}
                    <div>
                        <label className="mb-1.5 block text-sm font-medium text-slate-300">
                            Oponente
                        </label>
                        <select
                            className={selectClasses}
                            value={oponente}
                            onChange={(e) => setOponente(e.target.value)}
                        >
                            <option value="">Selecione um oponente</option>
                            {amigosOnline.map(amigo => (
                                <option key={amigo} value={amigo}>{amigo}</option>
                            ))}
                        </select>
                    </div>

                    {/* Lista 3 - Robô Lutador */}
                    <div>
                        <label className="mb-1.5 block text-sm font-medium text-slate-300">
                            Robô Lutador
                        </label>
                        <select
                            className={selectClasses}
                            value={roboSelecionado}
                            onChange={(e) => {
                                setRoboSelecionado(e.target.value);
                                setDeckSelecionado(""); // Reseta o deck ao trocar o Robô
                            }}
                        >
                            {meusRobos.length === 0 ? (
                                <option disabled>Vazio - Nenhum robô criado</option>
                            ) : (
                                <>
                                    <option value="">Selecione seu robô</option>
                                    {meusRobos.map(robo => (
                                        <option key={robo} value={robo}>{robo}</option>
                                    ))}
                                </>
                            )}
                        </select>
                    </div>

                    {/* Lista 4 - Deck (dependente da seleção anterior) */}
                    <div>
                        <label className="mb-1.5 block text-sm font-medium text-slate-300">
                            Deck
                        </label>
                        <select
                            className={selectClasses}
                            value={deckSelecionado}
                            onChange={(e) => setDeckSelecionado(e.target.value)}
                            disabled={!roboSelecionado} // Desabilita na ausência de robôs escolhidos
                        >
                            <option value="">Selecione o Deck</option>
                            {roboSelecionado && decksDoRobo[roboSelecionado]?.map(deck => (
                                <option key={deck} value={deck}>{deck}</option>
                            ))}
                        </select>
                        {!roboSelecionado && (
                            <p className="mt-1.5 text-xs text-slate-500">Selecione um robô para escolher o deck</p>
                        )}
                    </div>

                    <button
                        className="mt-2 w-full rounded-lg bg-gradient-to-r from-red-600 to-red-500 py-3 text-lg font-extrabold
                                   tracking-wide text-white shadow-lg shadow-red-600/30 transition
                                   hover:from-red-500 hover:to-red-400 hover:shadow-red-500/40
                                   active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-40
                                   disabled:hover:from-red-600 disabled:hover:to-red-500"
                        disabled={!podeLutar}
                    >
                        BOX!
                    </button>
                </div>
            </main>
        </div>
    );
}
