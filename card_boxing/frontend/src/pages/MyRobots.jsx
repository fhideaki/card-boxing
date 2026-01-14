import React, { useState } from "react";

export default function MyRobots() {
    // Estado para armazenar o que o usuário digita
    const [buscaRobo, setBuscaRobo] = useState("");

    // Estados para os filtros
    const [arquetipoSelecionado, setArquetipoSelecionado] = useState("");
    const [tipoFraquezaSelecionado, setTipoFraquezaSelecionado] = useState("");
    const [tipoResistenciaSelecionado, setTipoResistenciaSelecionado] = useState("");

    // Estados para a criação de robô (modal)
    const [modalAberto, setModalAberto] = useState(false);
    const [novoNome, setNovoNome] = useState("");
    const [novoArquetipo, setNovoArquetipo] = useState("");

    // Estados para as ações dos robôs
    const [modalEdicaoAberto, setModalEdicaoAberto] = useState(false);
    const [roboSendoEditado, setRoboSendoEditado] = useState(null);

    // Estados para as abas do modal (estilo Pokémon Showdown)
    const [abaAtual, setAbaAtual] = useState("menu");
    
    // Dados simulados dos robôs
    const listaRobos = [
        {
        id: 1,
        nome: "Sentinela de Ferro",
        arquetipo: "Tanque",
        fraquezas: ["Elétrico", "Água"],
        resistencias: ["Físico", "Físico", "Fogo"], // Exemplo de resistência duplicada
        constituicao: 10,
        forca: 8,
        agilidade: 2,
        hp: 200
    },
    {
        id: 2,
        nome: "Lâmina Veloz",
        arquetipo: "Atirador",
        fraquezas: ["Fogo"],
        resistencias: ["Vento", "Vento", "Vento"], // Resistência tripla
        constituicao: 4,
        forca: 5,
        agilidade: 12,
        hp: 120
    }
    ]

    // Dados simulados dos arquétipos
    const arquetiposDisponiveis = ["Tanque", "Atirador", "Suporte", "Assassino"];

    // Criando as opções dos dropdowns de forma dinâmica
    // Usando o objeto Set para garantir que não ocorram repetições
    const opcoesArquetipos = [...new Set(listaRobos.map(r => r.arquetipo))];
    const opcoesFraquezas = [...new Set(listaRobos.flatMap(r => r.fraquezas))]; 
    const opcoesResistencias = [...new Set(listaRobos.flatMap(r => r.resistencias))]; 

    // Lógica para a filtragem combinada
    const robosFiltrados = listaRobos.filter((robo) => {
        const bateNome = robo.nome.toLowerCase().includes(buscaRobo.toLowerCase());
        const bateArquetipo = arquetipoSelecionado === "" || robo.arquetipo === arquetipoSelecionado;
        const bateFraqueza = tipoFraquezaSelecionado === "" || robo.fraquezas.includes(tipoFraquezaSelecionado);
        const bateResistencia = tipoResistenciaSelecionado === "" || robo.resistencias.includes(tipoResistenciaSelecionado);

        return bateNome && bateArquetipo && bateFraqueza && bateResistencia;
    });

    return (
        <div>
            <h1>Meus Robôs</h1>

            {/* Campo de BuscaRobo */}
            <input
                type="text"
                placeholder="Digite o nome do robô..."
                value={buscaRobo}
                onChange={(e) => setBuscaRobo(e.target.value)}
            />

            <div>
                {/* Filtro de Arquétipo */}
                <div>
                    <label>Arquétipo: </label>
                    <select value={arquetipoSelecionado} onChange={(e) => setArquetipoSelecionado(e.target.value)}>
                        <option value="">Todos</option>
                        {opcoesArquetipos.map(a => <option key={a} value={a}>{a}</option>)}
                    </select>
                </div>

                {/* Filtro de Fraquezas */}
                <div>
                    <label>Fraquezas: </label>
                    <select value={tipoFraquezaSelecionado} onChange={(e) => setTipoFraquezaSelecionado(e.target.value)}>
                        <option value="">Todas</option>
                        {opcoesFraquezas.map(f => <option key={f} value={f}>{f}</option>)}
                    </select>
                </div>                
                
                {/* Filtro de Resistências */}
                <div>
                    <label>Resistências: </label>
                    <select value={tipoResistenciaSelecionado} onChange={(e) => setTipoResistenciaSelecionado(e.target.value)}>
                        <option value="">Todas</option>
                        {opcoesResistencias.map(r => <option key={r} value={r}>{r}</option>)}
                    </select>
                </div>

                {/* Botão para criar robô */}
                <div>
                    <button onClick={() => setModalAberto(true)}>Criar Robô</button>
                </div>
            </div>

            <table border="1">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nome</th>
                        <th>Arquétipo</th>
                        <th>Fraquezas</th>
                        <th>Resistências</th>
                        <th>Constituição</th>
                        <th>Força</th>
                        <th>Agilidade</th>
                        <th>HP</th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
                    {/* Usando a lista filtrada para o map */}
                    {robosFiltrados.map((robo) => (
                        <tr key={robo.id}>
                            <td>{robo.id}</td>
                            <td>{robo.nome}</td>
                            <td>{robo.arquetipo}</td>
                            <td>
                                {[...new Set(robo.fraquezas)].map(fra => {
                                    const quantidade = robo.fraquezas.filter(f => f === fra).length;
                                    return <span key={fra}>{fra} ({quantidade})</span>;
                                })}
                            </td>
                            <td>
                                {[...new Set(robo.resistencias)].map(res => {
                                    const quantidade = robo.resistencias.filter(r => r === res).length;
                                    return <span key={res}>{res} ({quantidade})</span>;
                                })}
                            </td>
                            <td>{robo.constituicao}</td>
                            <td>{robo.forca}</td>
                            <td>{robo.agilidade}</td>
                            <td>{robo.hp}</td>
                            <td>
                                <button onClick={() =>{
                                    setRoboSendoEditado(robo);
                                    setModalEdicaoAberto(true);
                                }}>
                                    Editar
                                </button>

                                <button onClick={() => {
                                    // Lógica simples de deletar, por enquanto é apenas um aviso ou filtro
                                    if(window.confirm(`Deseja deletar o robô ${robo.nome}?`)) {
                                        // Aqui vai entrar a função para excluir o robô
                                        console.log("Deletando robô com id: ", robo.id);
                                    }
                                }}>
                                    Deletar
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>  

            {/* Modal */}
            {modalAberto && (
                <div className="modal-overlay">
                    <div>
                        <h2>Criar Novo Robô</h2>

                        <div>
                            <label>Digite o nome do robô: </label>
                            <input
                                type="text"
                                value={novoNome}
                                onChange={(e) => setNovoNome(e.target.value)}
                            />
                        </div>

                        <div>
                            <label>Arquétipo: </label>
                            <select value={novoArquetipo} onChange={(e) => setNovoArquetipo(e.target.value)}>
                                <option value="">Selecione o arquétipo</option>
                                {arquetiposDisponiveis.map(arq => (
                                    <option key={arq} value={arq}>{arq}</option>
                                ))}
                            </select>
                        </div>
                        
                        {/* Botão para salvar o robô novo, preciso adicionar a lógica para inserir no banco de dados */}
                        <button onClick={() => setModalAberto(false)}>
                            Criar Robô
                        </button>
                        <button onClick={() => setModalAberto(false)}>Cancelar</button>
                    </div>
                </div>
            )}

            {/* Modal da edição */}
            {modalEdicaoAberto && (
                <div className="modal-overlay">
                    <div>
                        <label>Nome do Robô: </label>
                        <input
                            type="text"
                            value={roboSendoEditado?.nome || ""}
                            onChange={(e) => setRoboSendoEditado({
                                ...roboSendoEditado,
                                nome: e.target.value
                            })}
                        />
                        <button onClick={() => setModalEdicaoAberto(false)}>Fechar</button>
                    </div>

                    <hr />

                    {/* Janela em branco - Futuramente vai ser a parte de customizar peças e também os baralhos */}
                    <div>
                        {/* Abas do modal */}
                        {abaAtual === "menu" && (
                            <div>
                                <button
                                    onClick={() => setAbaAtual("pecas")}
                                >
                                    Peças
                                </button>
                                <button
                                    onClick={() => setAbaAtual("decks")}
                                >
                                    Decks
                                </button>
                            </div>
                        )}

                        {abaAtual === "pecas" && (
                            <div>
                                <button onClick={() => setAbaAtual("menu")}>Voltar</button>
                                <h3>Editor de Peças (Em Branco)</h3>
                                {/* Construir lógica das peças futuramente */}
                            </div>
                        )}

                        {abaAtual === "decks" && (
                            <div>
                                <button onClick={() => setAbaAtual("menu")}>Voltar</button>
                                <h3>Editor de Decks (Em Branco)</h3>
                                {/* Construir lógica dos decks futuramente */}
                            </div>
                        )}

                    </div>
                </div>
            )}
        </div>      
    )
}