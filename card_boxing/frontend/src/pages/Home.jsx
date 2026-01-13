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

    return (
        <div className="home-container">
            <main>
                {/* Lista 1 - Quantidade de Rounds */}
                <div>
                    <label>Quantidade de Rounds:</label>
                    <select value={rounds} onChange={(e) => setRounds(e.target.value)}>
                        {[1,3,5,7,9].map(num => (
                            <option key={num} value={num}>{num}</option>
                        ))}
                    </select>
                </div>                
                
                {/* Lista 2 - Oponente (Amigos Online) */}
                <div>
                    <label>Oponente:</label>
                    <select value={oponente} onChange={(e) => setOponente(e.target.value)}>
                        <option value="">Selecione um oponente</option>
                        {amigosOnline.map(amigo => (
                            <option key={amigo} value={amigo}>{amigo}</option>    
                        ))}
                    </select>
                </div>                
                
                {/* Lista 3 - Robô Lutador */}
                <div>
                    <label>Robô Lutador:</label>
                    <select 
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
                                <option value=""> Selecione seu robô</option>
                                {meusRobos.map(robo => (
                                    <option key={robo} value={robo}>{robo}</option>
                                ))}
                            </>
                        )}
                    </select>
                </div>

                {/* Lista 4 - Deck (dependente da seleção anterior) */}
                <div>
                    <label>Deck:</label>
                    <select 
                        value={deckSelecionado} 
                        onChange={(e) => setDeckSelecionado(e.target.value)}
                        disabled={!roboSelecionado} // Desabilita na ausência de robôs escolhidos
                    >
                        <option value="">Selecione o Deck</option>
                        {roboSelecionado && decksDoRobo[roboSelecionado]?.map(deck => (
                            <option key={deck} value={deck}>{deck}</option>
                        ))}    
                    </select>
                </div>
                
                <button>
                    BOX!
                </button>
            </main>
        </div>
    );
}