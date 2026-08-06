import React, { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

const CLASS_LABELS = { attack: "Ataque", guard: "Guarda", clinch: "Clinch" };
const CLASS_CLASSES = {
    attack: "border-red-500/60 text-red-300",
    guard: "border-sky-500/60 text-sky-300",
    clinch: "border-amber-500/60 text-amber-300",
};

const WINNER_LABELS = {
    player: { title: "Vitória!", classes: "text-emerald-400" },
    ai: { title: "Derrota", classes: "text-red-400" },
    draw: { title: "Empate", classes: "text-amber-400" },
};

const primaryBtn =
    "rounded-lg bg-gradient-to-r from-red-600 to-red-500 px-4 py-2 text-sm font-semibold text-white " +
    "shadow-sm shadow-red-600/30 transition hover:from-red-500 hover:to-red-400 disabled:cursor-not-allowed disabled:opacity-40";
const secondaryBtn =
    "rounded-lg border border-slate-700 bg-slate-800 px-4 py-2 text-sm font-semibold text-slate-200 transition hover:bg-slate-700";

function HpBar({ label, hp, maxHp }) {
    const pct = maxHp > 0 ? Math.max(0, Math.min(100, (hp / maxHp) * 100)) : 0;
    return (
        <div>
            <div className="mb-1 flex items-center justify-between text-sm">
                <span className="font-medium text-slate-200">{label}</span>
                <span className="text-slate-400">{Math.round(hp * 10) / 10} / {maxHp} HP</span>
            </div>
            <div className="h-3 w-full overflow-hidden rounded-full bg-slate-800">
                <div
                    className="h-full rounded-full bg-gradient-to-r from-red-600 to-red-500 transition-all"
                    style={{ width: `${pct}%` }}
                />
            </div>
        </div>
    );
}

export default function Battle() {
    const location = useLocation();
    const navigate = useNavigate();
    const { robotId, numRounds } = location.state || {};

    const [battle, setBattle] = useState(null);
    const [submitting, setSubmitting] = useState(false);

    useEffect(() => {
        if (!robotId) return;

        const iniciarBatalha = async () => {
            try {
                const resposta = await fetch('http://127.0.0.1:5000/api/battles', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ robot_id: robotId, num_rounds: numRounds || 1 })
                });
                const dados = await resposta.json();
                if (!resposta.ok) {
                    window.alert(dados.error || "Erro ao iniciar a batalha.");
                    return;
                }
                setBattle(dados);
            } catch (erro) {
                console.error("Erro ao iniciar batalha:", erro);
                window.alert("Erro ao iniciar a batalha.");
            }
        };

        iniciarBatalha();
    }, [robotId, numRounds]);

    const jogarCarta = async (cardId) => {
        if (!battle || submitting) return;
        setSubmitting(true);

        try {
            const resposta = await fetch(`http://127.0.0.1:5000/api/battles/${battle.battle_id}/turn`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ card_id: cardId })
            });
            const dados = await resposta.json();
            if (!resposta.ok) {
                window.alert(dados.error || "Erro ao jogar a carta.");
                return;
            }
            setBattle(dados);
        } catch (erro) {
            console.error("Erro ao jogar carta:", erro);
            window.alert("Erro ao jogar a carta.");
        } finally {
            setSubmitting(false);
        }
    };

    if (!robotId) {
        return (
            <div className="flex min-h-[calc(100vh-4rem)] items-center justify-center bg-slate-950 px-4">
                <div className="w-full max-w-md rounded-2xl border border-slate-800 bg-slate-900/60 p-8 text-center shadow-2xl">
                    <h1 className="text-xl font-bold text-white">Nenhuma luta configurada</h1>
                    <p className="mt-2 text-sm text-slate-400">Volte para a Home e escolha um robô para lutar.</p>
                    <button className={primaryBtn + " mt-6"} onClick={() => navigate('/')}>Voltar para Home</button>
                </div>
            </div>
        );
    }

    if (!battle) {
        return (
            <div className="flex min-h-[calc(100vh-4rem)] items-center justify-center bg-slate-950 px-4">
                <p className="text-slate-400">Preparando a luta...</p>
            </div>
        );
    }

    const finished = battle.status === 'finished';
    const winnerInfo = finished ? (WINNER_LABELS[battle.winner] || WINNER_LABELS.draw) : null;

    return (
        <div className="mx-auto max-w-4xl px-6 py-10">
            <div className="mb-6 text-center">
                <h1 className="text-2xl font-bold tracking-tight text-white">Round {battle.round}/{battle.num_rounds} · Turno {battle.turn}/{battle.turns_per_round}</h1>
            </div>

            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5 shadow-lg">
                    <HpBar label={battle.player.name} hp={battle.player.hp} maxHp={battle.player.max_hp} />
                    <p className="mt-3 text-xs text-slate-500">Deck: {battle.player.deck_remaining} · Cemitério: {battle.player.graveyard_count}</p>
                </div>
                <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5 shadow-lg">
                    <HpBar label={`${battle.opponent.name}`} hp={battle.opponent.hp} maxHp={battle.opponent.max_hp} />
                    <p className="mt-3 text-xs text-slate-500">
                        Mão: {battle.opponent.hand_count} · Deck: {battle.opponent.deck_remaining} · Cemitério: {battle.opponent.graveyard_count}
                    </p>
                </div>
            </div>

            {finished && (
                <div className="mt-6 rounded-2xl border border-slate-800 bg-slate-900/60 p-6 text-center shadow-2xl">
                    <h2 className={`text-3xl font-extrabold ${winnerInfo.classes}`}>{winnerInfo.title}</h2>
                    <p className="mt-1 text-sm text-slate-400">{battle.win_reason}</p>
                    <button className={primaryBtn + " mt-5"} onClick={() => navigate('/')}>Voltar para Home</button>
                </div>
            )}

            {!finished && (
                <div className="mt-6 rounded-2xl border border-slate-800 bg-slate-900/60 p-5 shadow-lg">
                    <h3 className="mb-3 text-sm font-semibold text-slate-300">Sua mão</h3>
                    <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
                        {battle.player.hand.map((card, index) => (
                            <button
                                key={`${card.id}-${index}`}
                                disabled={submitting}
                                onClick={() => jogarCarta(card.id)}
                                className={`rounded-lg border bg-slate-800/80 p-3 text-left transition hover:bg-slate-700
                                            disabled:cursor-not-allowed disabled:opacity-40 ${CLASS_CLASSES[card.class] || "border-slate-700 text-slate-300"}`}
                            >
                                <div className="flex items-center justify-between">
                                    <span className="font-semibold text-white">{card.name}</span>
                                    <span className="text-xs uppercase tracking-wide">{CLASS_LABELS[card.class] || card.class}</span>
                                </div>
                                <p className="mt-1 text-xs text-slate-400">{card.description}</p>
                            </button>
                        ))}
                    </div>
                </div>
            )}

            <div className="mt-6 rounded-xl border border-slate-800 bg-slate-900/60 p-4">
                <h3 className="mb-2 text-xs font-semibold uppercase tracking-wider text-slate-500">Registro da luta</h3>
                <div className="max-h-48 overflow-y-auto text-xs text-slate-400">
                    {battle.log.map((linha, i) => (
                        <p key={i}>{linha}</p>
                    ))}
                </div>
            </div>
        </div>
    );
}
