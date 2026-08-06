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

        if (total === DECK_SIZE) return <span className="text-emerald-400">Válido (10/10)</span>;
        if (total < DECK_SIZE) return <span className="text-amber-400">Incompleto ({total}/{DECK_SIZE})</span>;
        return <span className="text-red-400">Inválido ({total}/{DECK_SIZE})</span>;
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

    // Classes reutilizadas para manter consistência visual com o resto do app
    const inputClasses =
        "w-full rounded-lg border border-slate-700 bg-slate-800/80 px-4 py-2.5 text-slate-100 " +
        "shadow-sm transition placeholder:text-slate-500 focus:border-red-500 focus:outline-none focus:ring-2 focus:ring-red-500/40";
    const selectClasses =
        "w-full appearance-none rounded-lg border border-slate-700 bg-slate-800/80 px-3 py-2 text-sm text-slate-100 " +
        "shadow-sm transition focus:border-red-500 focus:outline-none focus:ring-2 focus:ring-red-500/40";
    const thClasses = "whitespace-nowrap px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-400";
    const primaryBtn =
        "rounded-lg bg-gradient-to-r from-red-600 to-red-500 px-4 py-2 text-sm font-semibold text-white " +
        "shadow-sm shadow-red-600/30 transition hover:from-red-500 hover:to-red-400 disabled:cursor-not-allowed disabled:opacity-40";
    const secondaryBtn =
        "rounded-lg border border-slate-700 bg-slate-800 px-4 py-2 text-sm font-semibold text-slate-200 transition hover:bg-slate-700";
    const dangerBtn =
        "rounded-lg border border-red-900/50 bg-red-950/30 px-3 py-1.5 text-sm font-medium text-red-400 transition hover:bg-red-900/40 hover:text-red-300";
    const modalOverlay = "fixed inset-0 z-50 flex items-center justify-center overflow-y-auto bg-black/60 px-4 py-8";

    return (
        <div className="mx-auto max-w-6xl px-6 py-10">
            <h1 className="text-2xl font-bold tracking-tight text-white">Meus Robôs</h1>

            {/* Campo de BuscaRobo */}
            <input
                type="text"
                placeholder="Digite o nome do robô..."
                value={buscaRobo}
                onChange={(e) => setBuscaRobo(e.target.value)}
                className={"mt-6 max-w-sm " + inputClasses}
            />

            <div className="mt-4 flex flex-wrap items-end gap-4">
                {/* Filtro de Arquétipo */}
                <div className="w-48">
                    <label className="mb-1.5 block text-sm font-medium text-slate-300">Arquétipo:</label>
                    <select className={selectClasses} value={arquetipoSelecionado} onChange={(e) => setArquetipoSelecionado(e.target.value)}>
                        <option value="">Todos</option>
                        {opcoesArquetipos.map(a => <option key={a} value={a}>{a}</option>)}
                    </select>
                </div>

                {/* Filtro de Fraquezas */}
                <div className="w-48">
                    <label className="mb-1.5 block text-sm font-medium text-slate-300">Fraquezas:</label>
                    <select className={selectClasses} value={tipoFraquezaSelecionado} onChange={(e) => setTipoFraquezaSelecionado(e.target.value)}>
                        <option value="">Todas</option>
                        {opcoesFraquezas.map(f => <option key={f} value={f}>{f}</option>)}
                    </select>
                </div>

                {/* Filtro de Resistências */}
                <div className="w-48">
                    <label className="mb-1.5 block text-sm font-medium text-slate-300">Resistências:</label>
                    <select className={selectClasses} value={tipoResistenciaSelecionado} onChange={(e) => setTipoResistenciaSelecionado(e.target.value)}>
                        <option value="">Todas</option>
                        {opcoesResistencias.map(r => <option key={r} value={r}>{r}</option>)}
                    </select>
                </div>

                {/* Botão para criar robô */}
                <div className="ml-auto">
                    <button className={primaryBtn} onClick={() => setModalAberto(true)}>+ Criar Robô</button>
                </div>
            </div>

            <div className="mt-6 overflow-x-auto rounded-xl border border-slate-800 shadow-lg">
                <table className="w-full border-collapse bg-slate-900/60 text-sm">
                    <thead className="bg-slate-800/80">
                        <tr>
                            <th className={thClasses}>ID</th>
                            <th className={thClasses}>Nome</th>
                            <th className={thClasses}>Arquétipo</th>
                            <th className={thClasses}>Fraquezas</th>
                            <th className={thClasses}>Resistências</th>
                            <th className={thClasses}>Constituição</th>
                            <th className={thClasses}>Força</th>
                            <th className={thClasses}>Agilidade</th>
                            <th className={thClasses}>HP</th>
                            <th className={thClasses}>Ações</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800">
                        {/* Usando a lista filtrada para o map */}
                        {robosFiltrados.map((robo) => (
                            <tr key={robo.id} className="transition hover:bg-slate-800/50">
                                <td className="whitespace-nowrap px-4 py-3 text-slate-300">{robo.id}</td>
                                <td className="whitespace-nowrap px-4 py-3 font-medium text-white">{robo.nome}</td>
                                <td className="whitespace-nowrap px-4 py-3 text-slate-300">{robo.arquetipo}</td>
                                <td className="px-4 py-3 text-slate-300">
                                    {[...new Set(robo.fraquezas)].map(fra => {
                                        const quantidade = robo.fraquezas.filter(f => f === fra).length;
                                        return <span key={fra} className="mr-1.5 inline-block">{fra} ({quantidade})</span>;
                                    })}
                                </td>
                                <td className="px-4 py-3 text-slate-300">
                                    {[...new Set(robo.resistencias)].map(res => {
                                        const quantidade = robo.resistencias.filter(r => r === res).length;
                                        return <span key={res} className="mr-1.5 inline-block">{res} ({quantidade})</span>;
                                    })}
                                </td>
                                <td className="whitespace-nowrap px-4 py-3 text-slate-300">{robo.constituicao}</td>
                                <td className="whitespace-nowrap px-4 py-3 text-slate-300">{robo.forca}</td>
                                <td className="whitespace-nowrap px-4 py-3 text-slate-300">{robo.agilidade}</td>
                                <td className="whitespace-nowrap px-4 py-3 text-slate-300">{robo.hp}</td>
                                <td className="whitespace-nowrap px-4 py-3">
                                    <div className="flex gap-2">
                                        <button className={secondaryBtn} onClick={() => abrirModalEdicao(robo)}>
                                            Editar
                                        </button>

                                        <button
                                            className={dangerBtn}
                                            onClick={() => {
                                                // Lógica simples de deletar, por enquanto é apenas um aviso ou filtro
                                                if(window.confirm(`Deseja deletar o robô ${robo.nome}?`)) {
                                                    handleDeletarRobo(robo.id);
                                                }
                                            }}
                                        >
                                            Deletar
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {/* Modal */}
            {modalAberto && (
                <div className={modalOverlay}>
                    <div className="w-full max-w-md rounded-2xl border border-slate-800 bg-slate-900 p-6 shadow-2xl">
                        <h2 className="mb-5 text-xl font-bold text-white">Criar Novo Robô</h2>

                        <div className="space-y-4">
                            <div>
                                <label className="mb-1.5 block text-sm font-medium text-slate-300">Digite o nome do robô:</label>
                                <input
                                    type="text"
                                    value={novoNome}
                                    onChange={(e) => setNovoNome(e.target.value)}
                                    className={inputClasses}
                                />
                            </div>

                            <div>
                                <label className="mb-1.5 block text-sm font-medium text-slate-300">Arquétipo:</label>
                                <select
                                    className={selectClasses}
                                    value={novoArquetipo} onChange={(e) => setNovoArquetipo(e.target.value)}>
                                    <option value="">Selecione o arquétipo</option>
                                    {arquetipos.map(arq => (
                                        <option key={arq.id} value={arq.id}>{arq.archetype_name}</option>
                                    ))}
                                </select>
                            </div>
                        </div>

                        {/* Botão para salvar o robô novo, preciso adicionar a lógica para inserir no banco de dados */}
                        <div className="mt-6 flex gap-2">
                            <button className={primaryBtn + " flex-1"} onClick={handleCriarRobo}>
                                Criar Robô
                            </button>
                            <button
                                className={secondaryBtn}
                                onClick={() => {
                                    setModalAberto(false);
                                    setNovoNome("");
                                    setNovoArquetipo("");
                                }}>Cancelar</button>
                        </div>
                    </div>
                </div>
            )}

            {/* Modal da edição */}
            {modalEdicaoAberto && (
                <div className={modalOverlay}>
                    <div className="w-full max-w-3xl rounded-2xl border border-slate-800 bg-slate-900 p-6 shadow-2xl">
                        <div className="flex items-end gap-3">
                            <div className="flex-1">
                                <label className="mb-1.5 block text-sm font-medium text-slate-300">Nome do Robô:</label>
                                <input
                                    type="text"
                                    value={roboSendoEditado?.nome || ""}
                                    onChange={(e) => setRoboSendoEditado({
                                        ...roboSendoEditado,
                                        nome: e.target.value
                                    })}
                                    className={inputClasses}
                                />
                            </div>
                            <button className={secondaryBtn} onClick={handleRenomear}>Renomear</button>
                            <button className={dangerBtn} onClick={() => setModalEdicaoAberto(false)}>Fechar</button>
                        </div>

                        <hr className="my-5 border-slate-800" />

                        {/* Janela em branco - Futuramente vai ser a parte de customizar peças e também os baralhos */}
                        <div>
                            {/* Abas do modal */}
                            {abaAtual === "menu" && (
                                <div className="flex gap-3">
                                    <button
                                        className={primaryBtn + " flex-1"}
                                        onClick={() => setAbaAtual("pecas")}
                                    >
                                        Peças
                                    </button>
                                    <button
                                        className={primaryBtn + " flex-1"}
                                        onClick={() => setAbaAtual("decks")}
                                    >
                                        Decks
                                    </button>
                                </div>
                            )}

                            {abaAtual === "pecas" && (
                                <div>
                                    <div className="mb-4 flex items-center justify-between">
                                        <button className={secondaryBtn} onClick={() => setAbaAtual("menu")}>← Voltar</button>
                                        <h3 className="text-lg font-bold text-white">Editor de Peças</h3>
                                        <div className="w-20" />
                                    </div>

                                    <div className="overflow-x-auto rounded-xl border border-slate-800">
                                        <table className="w-full border-collapse bg-slate-900/60 text-sm">
                                            <thead className="bg-slate-800/80">
                                                <tr>
                                                    <th className={thClasses}>Arquétipo</th>
                                                    <th className={thClasses}>Fraquezas</th>
                                                    <th className={thClasses}>Resistências</th>
                                                    <th className={thClasses}>CON</th>
                                                    <th className={thClasses}>FOR</th>
                                                    <th className={thClasses}>AGI</th>
                                                    <th className={thClasses}>HP</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                <tr>
                                                    <td className="whitespace-nowrap px-4 py-3 text-slate-300">{roboSendoEditado?.arquetipo}</td>
                                                    <td className="px-4 py-3 text-slate-300">
                                                        {[...new Set(listaTotal("fraquezas"))].map(fra => {
                                                            const qtd = listaTotal("fraquezas").filter(f => f === fra).length;
                                                            return <span key={fra} className="mr-1.5 inline-block">{fra} ({qtd}) </span>
                                                        })}</td>
                                                    <td className="px-4 py-3 text-slate-300">
                                                        {[...new Set(listaTotal("resistencias"))].map(res => {
                                                            const qtd = listaTotal("resistencias").filter(r => r === res).length;
                                                            return <span key={res} className="mr-1.5 inline-block">{res} ({qtd}) </span>
                                                        })}
                                                    </td>
                                                    <td className="whitespace-nowrap px-4 py-3 text-slate-300">{calcularTotal("conmod")}</td>
                                                    <td className="whitespace-nowrap px-4 py-3 text-slate-300">{calcularTotal("strmod")}</td>
                                                    <td className="whitespace-nowrap px-4 py-3 text-slate-300">{calcularTotal("agimod")}</td>
                                                    <td className="whitespace-nowrap px-4 py-3 text-slate-300">{calcularTotal("hpmod")}</td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>

                                    <div className="mt-5">
                                        <p className="mb-3 text-sm text-slate-400">Selecione as peças para os slots abaixo:</p>
                                        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                                            {slotsConfig.map((slot) => {
                                                // Criando uma chave única para o estado de cada equipamento
                                                const chaveSlot = slot.tecnico;
                                                const pecaEquipada = equipamento[chaveSlot];

                                                console.log(`Slot: ${chaveSlot} | Peça Encontrada:`, pecaEquipada);

                                                return (
                                                    <div key={slot.id}>
                                                        <label className="mb-1.5 block text-sm font-medium text-slate-300">{slot.label}:</label>
                                                        <select
                                                            className={selectClasses}
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
                                    <div className="mt-6">
                                        <button
                                            className={primaryBtn + " w-full"}
                                            onClick={handleSalvarPecas}
                                        >
                                            Salvar Configuração de Peças
                                        </button>
                                    </div>
                                </div>
                            )}

                            {abaAtual === "decks" && (
                                <div>
                                    <h3 className="text-lg font-bold text-white">Editor de Decks - {roboSendoEditado?.nome}</h3>
                                    <div className="mt-3 mb-4 flex items-center justify-between">
                                        <button className={secondaryBtn} onClick={() => setAbaAtual("menu")}>← Voltar</button>
                                        <strong className="text-sm text-slate-300">Status: {verificarStatusDeck(deckAtual)}</strong>
                                    </div>

                                    <div className="overflow-x-auto rounded-xl border border-slate-800">
                                        <table className="w-full border-collapse bg-slate-900/60 text-sm">
                                            <thead className="bg-slate-800/80">
                                                <tr>
                                                    <th className={thClasses}>ID</th>
                                                    <th className={thClasses}>Nome da Carta</th>
                                                    <th className={thClasses}>Quantidade</th>
                                                    <th className={thClasses}>Ações</th>
                                                </tr>
                                            </thead>
                                            <tbody className="divide-y divide-slate-800">
                                                {deckAtual.map((carta) => (
                                                    <tr key={carta.id} className="transition hover:bg-slate-800/50">
                                                        <td className="whitespace-nowrap px-4 py-3 text-slate-300">{carta.id}</td>
                                                        <td className="whitespace-nowrap px-4 py-3 font-medium text-white">{carta.name}</td>
                                                        <td className="whitespace-nowrap px-4 py-3 text-slate-300">{carta.quantity} / {carta.max_inventory}</td>
                                                        <td className="whitespace-nowrap px-4 py-3">
                                                            <div className="flex gap-2">
                                                                <button
                                                                    className="h-7 w-7 rounded-md border border-slate-700 bg-slate-800 font-bold text-slate-200 transition hover:bg-slate-700"
                                                                    onClick={() => alterarQuantidadeCarta(carta.id, -1)}
                                                                >-</button>
                                                                <button
                                                                    className="h-7 w-7 rounded-md border border-slate-700 bg-slate-800 font-bold text-slate-200 transition hover:bg-slate-700"
                                                                    onClick={() => alterarQuantidadeCarta(carta.id, 1)}
                                                                >+</button>
                                                            </div>
                                                        </td>
                                                    </tr>
                                                ))}
                                            </tbody>
                                        </table>
                                    </div>

                                    {/* Botão para enviar o estado deckAtual consolidado para o Backend */}
                                    <button
                                        className={primaryBtn + " mt-5 w-full"}
                                        disabled={deckAtual.reduce((acc, c) => acc + c.quantity, 0) !== 10}
                                        onClick={salvarDeckNoBanco}>
                                        Salvar Deck
                                    </button>
                                </div>
                            )}

                        </div>
                    </div>
                </div>
            )}
        </div>
    )
}
