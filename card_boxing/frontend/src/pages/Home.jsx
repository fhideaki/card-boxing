import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Home() {
    const navigate = useNavigate();

    // 1 - Estados para armazenar o que o usuário selecionou
    const [rounds, setRounds] = useState(1);
    const [roboSelecionado, setRoboSelecionado] = useState("");

    // 2 - Dados reais vindos do Backend
    const [meusRobos, setMeusRobos] = useState([]);
    const [deckStatus, setDeckStatus] = useState(null); // { total, pronto }

    useEffect(() => {
        const carregarRobos = async () => {
            try {
                const resposta = await fetch('http://127.0.0.1:5000/api/robots?user_id=1');
                const dados = await resposta.json();
                setMeusRobos(dados.robots || []);
            } catch (erro) {
                console.error("Erro ao buscar robôs:", erro);
            }
        };

        carregarRobos();
    }, []);

    useEffect(() => {
        if (!roboSelecionado) {
            setDeckStatus(null);
            return;
        }

        const carregarDeck = async () => {
            try {
                const resposta = await fetch(`http://127.0.0.1:5000/api/${roboSelecionado}/deck`);
                const dados = await resposta.json();
                const total = (dados.cartas || []).reduce((acc, c) => acc + c.quantity, 0);
                setDeckStatus({ total, pronto: total === 10 });
            } catch (erro) {
                console.error("Erro ao buscar deck:", erro);
                setDeckStatus(null);
            }
        };

        carregarDeck();
    }, [roboSelecionado]);

    const deckPronto = deckStatus?.pronto ?? false;
    const podeLutar = roboSelecionado && deckPronto;

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

                    {/* Adversário - por enquanto só vs. IA */}
                    <div>
                        <label className="mb-1.5 block text-sm font-medium text-slate-300">
                            Adversário
                        </label>
                        <div className="w-full rounded-lg border border-slate-700 bg-slate-800/40 px-4 py-2.5 text-slate-300">
                            Computador (IA)
                        </div>
                    </div>

                    {/* Lista 2 - Robô Lutador */}
                    <div>
                        <label className="mb-1.5 block text-sm font-medium text-slate-300">
                            Robô Lutador
                        </label>
                        <select
                            className={selectClasses}
                            value={roboSelecionado}
                            onChange={(e) => setRoboSelecionado(e.target.value)}
                        >
                            {meusRobos.length === 0 ? (
                                <option disabled>Vazio - Nenhum robô criado</option>
                            ) : (
                                <>
                                    <option value="">Selecione seu robô</option>
                                    {meusRobos.map(robo => (
                                        <option key={robo.id} value={robo.id}>{robo.name} ({robo.archetype})</option>
                                    ))}
                                </>
                            )}
                        </select>
                    </div>

                    {/* Status do Deck (dependente da seleção anterior) */}
                    {roboSelecionado && (
                        <div>
                            <label className="mb-1.5 block text-sm font-medium text-slate-300">
                                Deck
                            </label>
                            {deckStatus ? (
                                <p className={`text-sm ${deckPronto ? "text-emerald-400" : "text-amber-400"}`}>
                                    {deckPronto
                                        ? `Deck: ${deckStatus.total}/10 pronto`
                                        : `Deck: ${deckStatus.total}/10 incompleto — configure em Meus Robôs`}
                                </p>
                            ) : (
                                <p className="text-sm text-slate-500">Carregando deck...</p>
                            )}
                        </div>
                    )}

                    <button
                        className="mt-2 w-full rounded-lg bg-gradient-to-r from-red-600 to-red-500 py-3 text-lg font-extrabold
                                   tracking-wide text-white shadow-lg shadow-red-600/30 transition
                                   hover:from-red-500 hover:to-red-400 hover:shadow-red-500/40
                                   active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-40
                                   disabled:hover:from-red-600 disabled:hover:to-red-500"
                        disabled={!podeLutar}
                        onClick={() => navigate('/battle', {
                            state: { robotId: Number(roboSelecionado), numRounds: Number(rounds) }
                        })}
                    >
                        BOX!
                    </button>
                </div>
            </main>
        </div>
    );
}
