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
                carregarRobos();
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
    const [equipamento, setEquipamento] = useState({});

    // Estados para as abas do modal (estilo Pokémon Showdown)
    const [abaAtual, setAbaAtual] = useState("menu");

    // Dados dos robôs
    const [meusRobos, setMeusRobos] = useState([]);

    // Função para pegar as peças já equipadas nos robôs criados
    const abrirModalEdicao = (robo) => {
        setRoboSendoEditado(robo);
        setAbaAtual("menu");

        // Limpa o estado anterior e preenche com as peças já equipadas
        const pecasAtuais = {};

        if (robo.pecas && robo.pecas.length > 0) {
            robo.pecas.forEach(p => {
                pecasAtuais[p.slot] = { id: p.id, nome: p.nome };
            });
        }
        setEquipamento(pecasAtuais);

        fetch(`http://127.0.0.1:5000/api/${robo.id}/deck`)
            .then(res => res.json())
            .then(data => {
                console.log("Dados recebidos da API:", data);
                setDeckAtual(data.cartas || []);
            })
            .catch(err => console.error('Erro ao carregar deck:', err));

        setModalEdicaoAberto(true);
    };

    const carregarRobos = () => {
        fetch('http://127.0.0.1:5000/api/robots?user_id=1')
            .then(res => res.json())
            .then(data => {
                const robosServidor = data.robots || [];

                // Mapeando o nome das chaves do banco
                const robosFormatados = robosServidor.map(r => ({
                    id: r.id,
                    nome: r.name,
                    arquetipo: r.archetype,

                    constituicao: r.stats.constitution,
                    forca: r.stats.strength,
                    agilidade: r.stats.agility,
                    hp: r.stats.hp,

                    pecas: r.parts || [],
                    fraquezas: r.fraquezas || [],
                    resistencias: r.resistencias || []
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

    useEffect(() => {
        carregarRobos();
        carregarSlots();
        carregarPecas();
    }, []); 

    // Dados dos slots
    const [slotsConfig, setSlotsConfig] = useState([]);

    const carregarSlots = () => {
        fetch('http://127.0.0.1:5000/api/slots')
            .then(res => res.json())
            .then(data => {
                // Mapeando o que vem do banco
                const slotsFormatados = data.map(s => ({
                    id: s.id,
                    tecnico: s.slot_name,
                    label: s.slot_name
                }));

                setSlotsConfig(slotsFormatados);
            })
            .catch(err => console.error("Erro ao carregar slots>", err));
    };
    // Dados das peças
    const [listaPecas, setListaPecas] = useState([]);

    const carregarPecas = () => {
        fetch('http://127.0.0.1:5000/api/parts')
            .then(res => res.json())
            .then(data => {
                setListaPecas(data);
            })
            .catch(err => console.error("Erro ao carregar peças:", err));
    };

    // Estado para renomar o robô
    const handleRenomear = () => {
        fetch(`http://127.0.0.1:5000/api/${roboSendoEditado.id}/rename`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: roboSendoEditado.nome })
        })
        .then(res => {
            if (res.ok) {
                alert("Nome alterado com sucesso!");
                setModalEdicaoAberto(false);
                carregarRobos();
            } else {
                alert("Erro ao renomear.");
            }
        });
    };

    // Estado para atualizar as peças
    const handleSalvarPecas = () => {
        const listaParaEnviar = slotsConfig.map(slot => {
            const pecaNoEstado = equipamento[slot.tecnico];
            return {
                slot_id: slot.id,
                part_id: pecaNoEstado ? pecaNoEstado.id : null
            };
        });

        fetch(`http://127.0.0.1:5000/api/${roboSendoEditado.id}/equip`, {
            method: 'PATCH', 
            headers: { 'Content-Type': 'application/json' },
            body: JSON. stringify({ parts: listaParaEnviar })
        })
        .then(res => {
            if (res.ok) {
                alert("Peças salvas com sucesso!");
                carregarRobos();
            } else {
                alert("Erro ao salvar peças.");
            }
        })
        .catch(err => console.error("Erro:", err));
    };

    // Dados dos decks
    const [deckAtual, setDeckAtual] = useState([]);

    //Verificação do estado do deck
    const verificarStatusDeck = (cartas) => {
        const total = cartas.reduce((acc, c) => acc + c.quantity, 0);
        const DECK_SIZE = 10;

        if (total === DECK_SIZE) return <span style={{color: "green"}}>Válido (10/10)</span>;
        if (total < DECK_SIZE) return <span style={{color: "orange"}}>Incompleto ({total}/{DECK_SIZE})</span>;
        return <span style={{color: "red"}}>Inválido ({total}/{DECK_SIZE})</span>;
    };

    // Salvar deck no banco de dados
    const salvarDeckNoBanco = () => {
        // Filtrando apenas as cartas que possuem quantidade maior que 0 para enviar
        const cartasParaSalvar = deckAtual.filter(c => c.quantity > 0);

        fetch(`http://127.0.0.1:5000/api/${roboSendoEditado.id}/deck`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ cartas: cartasParaSalvar })
        })
        .then(async res => {
            const data = await res.json();
            if (res.ok) {
                alert(data.message);
                setAbaAtual("menu");
            } else {
                alert("Erro: " + data.error);
            }
        })
        .catch(err => console.error("Erro ao salvar:", err));
    };

    // Função para incrementar/decrementar a quantidade no estado
    const alterarQuantidadeCarta = (cartaId, incremento) => {
        const DECK_SIZE = 10;
        const totalAtual = deckAtual.reduce((acc, c) => acc + c.quantity, 0);

        setDeckAtual(prevDeck => {
            return prevDeck.map(c => {
                if (c.id === cartaId) {
                    const novaQtd = c.quantity + incremento;

                    // Validações locais (front)
                    // Não pode ser menor que 0
                    if (novaQtd < 0) return c;
                    // Não pode ser maior do que o jogador possui no inventário
                    if (novaQtd > c.max_inventory) return c;
                    // Não pode ser maior que o limite de duplicatas
                    if (incremento > 0 && novaQtd > 3) return c;
                    // Não pode passar o total de 15 cartas no deck
                    if (incremento > 0 && totalAtual >= DECK_SIZE) return c;

                    return { ...c, quantity: novaQtd };
                }
                return c;
            });
        });
    };

    // Criando as opções dos dropdowns de forma dinâmica
    // Usando o objeto Set para garantir que não ocorram repetições
    const opcoesArquetipos = [...new Set(meusRobos.map(r => r.arquetipo))];
    const opcoesFraquezas = [...new Set(meusRobos.flatMap(r => r.fraquezas))]; 
    const opcoesResistencias = [...new Set(meusRobos.flatMap(r => r.resistencias))]; 

    // Lógica para a filtragem combinada
    const robosFiltrados = meusRobos.filter((robo) => {
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

    // Função para deletar um robô
    const handleDeletarRobo = (id) => {
        fetch(`http://127.0.0.1:5000/api/${id}`, {
            method: 'DELETE',
        })
        .then(res => {
            if (res.ok) {
                alert("Robô deletado!");
                carregarRobos();
            } else {
                alert("Erro ao deletar robô.");
            }
        })
        .catch(err => console.error("Erro ao deletar:", err));
    };

    // Função para atualizar os dados do modal das cartas
    useEffect(() => {
        if (abaAtual === "decks" && roboSendoEditado) {
            fetch(`http://127.0.0.1:5000/api/${roboSendoEditado.id}/deck`)
                .then(res => res.json())
                .then(data => {
                setDeckAtual(data.cartas || []);
            })
            .catch(err => console.error("Erro ao recarregar deck:", err));
        }
    }, [abaAtual, roboSendoEditado]);

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
                                <button onClick={() => abrirModalEdicao(robo)}>
                                    Editar
                                </button>

                                <button onClick={() => {
                                    // Lógica simples de deletar, por enquanto é apenas um aviso ou filtro
                                    if(window.confirm(`Deseja deletar o robô ${robo.nome}?`)) {
                                        handleDeletarRobo(robo.id);
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
                        <button onClick={handleRenomear}>Renomear</button>
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
                                        {slotsConfig.map((slot) => {
                                            // Criando uma chave única para o estado de cada equipamento
                                            const chaveSlot = slot.tecnico;
                                            const pecaEquipada = equipamento[chaveSlot];

                                            console.log(`Slot: ${chaveSlot} | Peça Encontrada:`, pecaEquipada);

                                            return (
                                                <div key={slot.id}>
                                                    <label>{slot.label}:</label>
                                                    <select
                                                        value={pecaEquipada?.id || ""}
                                                        onChange={(e) => {
                                                            const idSelecionado = parseInt(e.target.value);
                                                            const pecaEncontrada = listaPecas.find(p => p.id === idSelecionado);

                                                            setEquipamento(prev => ({
                                                                ...prev,
                                                                [chaveSlot]: pecaEncontrada || null
                                                            }));
                                                        }}
                                                    >
                                                        <option value="">(Nenhuma)</option>
                                                        {listaPecas
                                                            .filter(p => p.slot === slot.tecnico)
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
                                <div>
                                    <button
                                        onClick={handleSalvarPecas}
                                    >
                                        Salvar Configuração de Peças
                                    </button>
                                </div>
                            </div>
                        )}

                        {abaAtual === "decks" && (
                            <div>
                                <h3>Editor de Decks - {roboSendoEditado?.nome}</h3>
                                <div>
                                    <button onClick={() => setAbaAtual("menu")}>Voltar</button>
                                    <strong> Status: {verificarStatusDeck(deckAtual)}</strong>
                                </div>

                                <table>
                                    <thead>
                                        <tr>
                                            <th>ID</th>
                                            <th>Nome da Carta</th>
                                            <th>Quantidade</th>
                                            <th>Ações</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {deckAtual.map((carta) => (
                                            <tr key={carta.id}>
                                                <td>{carta.id}</td>
                                                <td>{carta.name}</td>
                                                <td>{carta.quantity} / {carta.max_inventory}</td>
                                                <td>
                                                    <button onClick={() => alterarQuantidadeCarta(carta.id, -1)}>-</button>
                                                    <button onClick={() => alterarQuantidadeCarta(carta.id, 1)}>+</button>
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>

                                {/* Botão para enviar o estado deckAtual consolidado para o Backend */}
                                <button
                                    disabled={deckAtual.reduce((acc, c) => acc + c.quantity, 0) !== 10}
                                    onClick={salvarDeckNoBanco}>
                                    Salvar Deck
                                </button>
                            </div>
                        )}

                    </div>
                </div>
            )}
        </div>      
    )
}