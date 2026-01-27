import React, { useEffect, useState } from "react";

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

    // Estado para salvar o robô criado
    const handleCriarRobo = () => {
        // Validação Básica
        if (!novoNome || !novoArquetipo) {
            alert("Preencha todos os campos!");
            return;
        }

        // Montagem do objeto para o backend
        const payload = {
            robot_name: novoNome,
            archetype_id: parseInt(novoArquetipo)
        };

        // Chamada para a API
        fetch('http://127.0.0.1:5000/api/robots', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        })
        .then(res => {
            if (res.ok) {
                alert("Robô criado com sucesso!");
                setModalAberto(false); // Fecha o modal
                setNovoNome(""); // Limpa os campos
                setNovoArquetipo(""); 
            } else {
                alert("Erro ao criar robô.");
            }
        })
        .catch(err => console.error("Erro ao salvar:", err));
    }

    // Estados para as ações dos robôs
    const [modalEdicaoAberto, setModalEdicaoAberto] = useState(false);
    const [roboSendoEditado, setRoboSendoEditado] = useState(null);

    // Estado para carregar as peças
    const [equipamento, setEquipamento] = useState(roboSendoEditado?.slots || {});

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

    // Dados dos robôs
    const [meusRobos, setMeusRobos] = useState([]);

    const carregarRobos = () => {
        fetch('http://127.0.0.1:5000/api/robots?user_id=1')
            .then(res => res.json())
            .then(data => {
                // Mapeando o nome das chaves do banco
                const robosFormatados = data.map(r => ({
                    id: r.id,
                    nome: r.name,
                    arquetipo: r.archetype,

                    constituicao: r.stats.constitution,
                    forca: r.stats.strength,
                    agilidade: r.stats.agility,
                    hp: r.stats.hp,

                    pecas: r.parts || [],
                    fraquezas: [],
                    resistencias: []
                }));

                setMeusRobos(robosFormatados);
            })
            .catch(err => console.error("Erro ao carregar robôs:", err));
    };

    // Dados dos arquétipos
    const [arquetipos, setArquetipos] = useState([]);

    useEffect(() => {
        // Buscando os arquétipos para dropdown no modal
        fetch('http://127.0.0.1:5000/api/archetypes')
            .then(res => res.json())
            .then(data => setArquetipos(data))
            .catch(err => console.error("Erro ao buscar arquétipos:", err));
    }, []);

    // Dados simulados dos slots
    const slotsConfig = [
    { id: "Cabeça", label: "Cabeça" },
    { id: "Peito", label: "Corpo" },
    { id: "Braço", label: "Braço Direito" },
    { id: "Braço", label: "Braço Esquerdo" },
    { id: "Pernas", label: "Perna Direita" },
    { id: "Pernas", label: "Perna Esquerda" },
    { id: "Costas", label: "Costas" }
    ];

    // Dados simulados das peças
    const listaPecas = [
    {
        id: 1,
        nome: "Núcleo de Energia Simples",
        slot: "Peito",
        tipo: "Eletrônico",
        conmod: 5,
        strmod: 0,
        agimod: 0,
        hpmod: 50,
        fraquezas: ["Água"],
        resistencias: ["Físico"],
        liberaCartas: [
            { carta: "Recarregar", precisaDe: null }
        ]
    },
    {
        id: 2,
        nome: "Processador de Combate",
        slot: "Cabeça",
        tipo: "Eletrônico",
        conmod: 0,
        strmod: 2,
        agimod: 3,
        hpmod: 10,
        fraquezas: ["Elétrico"],
        resistencias: [],
        liberaCartas: [
            { carta: "Análise de Dados", precisaDe: null }
        ]
    },
    {
        id: 3,
        nome: "Tanque de Combustível",
        slot: "Costas",
        tipo: "Suporte",
        conmod: 3,
        strmod: 0,
        agimod: -1,
        hpmod: 20,
        fraquezas: ["Fogo"],
        resistencias: ["Explosão"],
        liberaCartas: [
            { carta: "Explosão de Nafta", precisaDe: "Lançador de Chamas" }
        ]
    },
    {
        id: 4,
        nome: "Lançador de Chamas",
        slot: "Braço",
        tipo: "Fogo",
        conmod: 0,
        strmod: 4,
        agimod: 0,
        hpmod: 15,
        fraquezas: ["Água"],
        resistencias: ["Fogo"],
        liberaCartas: [
            { carta: "Incinerar", precisaDe: null },
            { carta: "Explosão de Nafta", precisaDe: "Tanque de Combustível" }
        ]
    },
    {
        id: 5,
        nome: "Propulsor Hidráulico",
        slot: "Pernas",
        tipo: "Mecânico",
        conmod: 2,
        strmod: 0,
        agimod: 5,
        hpmod: 30,
        fraquezas: ["Gelo"],
        resistencias: ["Físico"],
        liberaCartas: [
            { carta: "Investida", precisaDe: null }
        ]
    },
    {
        id: 6,
        nome: "Placa de Titânio",
        slot: "Peito",
        tipo: "Defesa",
        conmod: 8,
        strmod: -1,
        agimod: -2,
        hpmod: 100,
        fraquezas: [],
        resistencias: ["Físico", "Físico"], // Exemplo de resistência dupla
        liberaCartas: []
    }
    ];

    // Dados simulados dos decks
    const [listaDecks, setListaDecks] = useState([
        { id: 1, nome: "Deck Inicial", cartas: [] },
        { id: 2, nome: "Deck de Fogo", cartas: [] }
    ]);

    //Verificação do estado do deck
    const verificarStatusDeck = (deck) => {
    // No futuro, aqui compararemos deck.cartas com as cartas liberadas pelas peças em 'equipamento'
    // Por enquanto, vamos retornar "Válido" apenas para ilustrar
        return "Válido"; 
    };

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

    // Lógica para somar os atributos do que estiver equipado
    const calcularTotal = (atributo) => {
        // Começa com o valor base (se houver) ou zero
        let total = 0;

        // Percorre os slots e soma os atributos correspondentes para cada peça
        Object.values(equipamento).forEach(peca => {
            if (peca) total += peca[atributo] || 0;
        });
        return total;
    };

    // Para fraquezas e resistências, somando as ocorrências nas listas
    const listaTotal = (campo) => {
        const todos = [];
        Object.values(equipamento).forEach(peca => {
            if (peca && peca[campo]) todos.push(...peca[campo]);
        });
        return todos; 
    };

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
                            <select 
                                value={novoArquetipo} onChange={(e) => setNovoArquetipo(e.target.value)}>
                                <option value="">Selecione o arquétipo</option>
                                {arquetipos.map(arq => (
                                    <option key={arq.id} value={arq.id}>{arq.archetype_name}</option>
                                ))}
                            </select>
                        </div>
                        
                        {/* Botão para salvar o robô novo, preciso adicionar a lógica para inserir no banco de dados */}
                        <button onClick={handleCriarRobo}>
                            Criar Robô
                        </button>
                        <button onClick={() => {
                            setModalAberto(false);
                            setNovoNome("");
                            setNovoArquetipo("");
                            }}>Cancelar</button>
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
                                <h3>Editor de Peças</h3>

                                <table>
                                    <thead>
                                        <tr>
                                            <th>Arquétipo</th>
                                            <th>Fraquezas</th>
                                            <th>Resistências</th>
                                            <th>CON</th>
                                            <th>FOR</th>
                                            <th>AGI</th>
                                            <th>HP</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td>{roboSendoEditado?.arquetipo}</td>
                                            <td>
                                                {[...new Set(listaTotal("fraquezas"))].map(fra => {
                                                    const qtd = listaTotal("fraquezas").filter(f => f === fra).length;
                                                    return <span key={fra}>{fra} ({qtd}) </span>
                                                })}</td>
                                            <td>
                                                {[...new Set(listaTotal("resistencias"))].map(res => {
                                                    const qtd = listaTotal("resistencias").filter(r => r === res).length;
                                                    return <span key={res}>{res} ({qtd}) </span>
                                                })}
                                            </td>
                                            <td>{calcularTotal("conmod")}</td>
                                            <td>{calcularTotal("strmod")}</td>
                                            <td>{calcularTotal("agimod")}</td>
                                            <td>{calcularTotal("hpmod")}</td>
                                        </tr>
                                    </tbody>
                                </table>
                                <div>
                                    <p>Selecione as peças para os slots abaixo:</p>
                                    <div>
                                        {slotsConfig.map((slot, index) => {
                                            // Criando uma chave única para o estado de cada equipamento
                                            const chaveSlot = `${slot.id}_${index}`;
                                            const pecaEquipada = equipamento[chaveSlot];

                                            return (
                                                <div>
                                                    <label>{slot.label}:</label>
                                                    <select
                                                        value={pecaEquipada?.id || ""}
                                                        onChange={(e) => {
                                                            const idSelecionado = parseInt(e.target.value);
                                                            const pecaEncontrada = listaPecas.find(p => p.id === idSelecionado);

                                                            // Atualiza o estado mantendo as outras peças e trocando somente a selecionada
                                                            setEquipamento(prev => ({
                                                                ...prev,
                                                                [chaveSlot]: pecaEncontrada || null
                                                            }));
                                                        }}>
                                                            <option value="">(Nenhuma)</option>
                                                            {/* Filtrando a lista global para mostrar apenas peças deste slot */}
                                                            {listaPecas
                                                                .filter(p => p.slot === slot.id)
                                                                .map(p => (
                                                                    <option key={p.id} value={p.id}>{p.nome}</option>
                                                                ))
                                                            }
                                                        </select>
                                                </div>
                                            )
                                        })}
                                    </div>
                                </div>
                            </div>
                        )}

                        {abaAtual === "decks" && (
                            <div>
                                <h3>Editor de Decks</h3>
                                <div>
                                    <button onClick={() => setAbaAtual("menu")}>Voltar</button>
                                    <button onClick={() => {/* Lógica para novo deck */}}>Criar novo deck</button>
                                </div>

                                <table>
                                    <thead>
                                        <tr>
                                            <th>#</th>
                                            <th>Nome do Deck</th>
                                            <th>Estado</th>
                                            <th>Ações</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {listaDecks.map((deck, index) => (
                                            <tr key={deck.id}>
                                                <td>{index + 1}</td>
                                                <td>{deck.nome}</td>
                                                <td>{verificarStatusDeck(deck)}</td>
                                                <td>
                                                    <button onClick={() => {/* Abrir editor do deck */}}>
                                                        Editar
                                                    </button>
                                                    <button onClick={() => {/* Deletar Deck */}}>
                                                        Excluir
                                                    </button>
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        )}

                    </div>
                </div>
            )}
        </div>      
    )
}