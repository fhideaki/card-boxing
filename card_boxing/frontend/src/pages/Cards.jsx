import React, { useEffect, useState } from "react";

export default function Cards() {
    // Estado para armazenar o que o usuário digita
    const [buscaCarta, setBuscaCarta] = useState("");

    // Estado para armazenar a ordenação da tabela
    const [ordenacao, setOrdenacao] = useState({ coluna: null, direcao: null });

    // Estados para os filtros
    const [classeSelecionada, setClasseSelecionada] = useState("");
    const [tipoSelecionado, setTipoSelecionado] = useState("");
    const [pecaSelecionada, setPecaSelecionada] = useState("");

    // Dados simulados das cartas
    const [listaCartas, setListaCartas] = useState([]);

    useEffect(() =>{
        const carregarCartas = async () => {
            try {
                const resposta = await fetch('http://127.0.0.1:5000/api/cards');
                const dados = await resposta.json();
                setListaCartas(dados);
            } catch (erro) {
                console.error("Erro ao buscar cartas:", erro);
            }
        };

        carregarCartas();
    }, []);

    // Criando as opções dos dropdowns de forma dinâmica
    // Usando o objeto Set para garantir que não ocorram repetições
    const opcoesClasse = [...new Set(listaCartas.map(c => c.class))];
    const opcoesTipos = [...new Set(listaCartas.map(c => c.tipo_nome))];
    // Para as peças, pode existir uma lista, então ela precisa ser achatada antes.
    const opcoesPecas = [...new Set(listaCartas.flatMap(c => c.requisitos_pecas))];

    // Lógica para a filtragem combinada
    const cartasFiltradas = listaCartas.filter((carta) => {
        const bateNome = carta.nome.toLowerCase().includes(buscaCarta.toLowerCase());
        const bateClasse = classeSelecionada === "" || carta.class === classeSelecionada;
        const bateTipo = tipoSelecionado === "" || carta.tipo_nome === tipoSelecionado;
        const batePeca = pecaSelecionada === "" || carta.requisitos_pecas.includes(pecaSelecionada);

        return bateNome && bateClasse && bateTipo && batePeca;
    });

    // Lógica para ordernar a filtragem
    const cartasFiltradasEOrdenadas = [...cartasFiltradas].sort((a, b) => {
        if (!ordenacao.coluna || !ordenacao.direcao) return 0;

        const valorA = a[ordenacao.coluna];
        const valorB = b[ordenacao.coluna];

        if (valorA < valorB) return ordenacao.direcao === 'asc' ? -1 : 1;
        if (valorA > valorB) return ordenacao.direcao === 'asc' ? 1 : -1;
        return 0;
    });

    // Criando o componente de cabeçalho para ordenação
    const handleSort = (coluna) => {
        setOrdenacao(prev => {
            if (prev.coluna !== coluna) return { coluna, direcao: 'asc' };
            if (prev.direcao === 'asc') return { coluna, direcao: 'desc' };
            return { coluna: null, direcao: null }
        });
    };

    // Ícone visual
    const renderSeta = (coluna) => {
        if (ordenacao.coluna !== coluna) return " ↕";
        if (ordenacao.direcao === 'asc') return " ▲";
        if (ordenacao.direcao === 'desc') return " ▼";
    };

    const selectClasses =
        "w-full appearance-none rounded-lg border border-slate-700 bg-slate-800/80 px-3 py-2 text-sm text-slate-100 " +
        "shadow-sm transition focus:border-red-500 focus:outline-none focus:ring-2 focus:ring-red-500/40";

    const thClasses =
        "cursor-pointer select-none whitespace-nowrap px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider " +
        "text-slate-400 transition hover:text-white";

    return (
        <div className="mx-auto max-w-6xl px-6 py-10">
            <h1 className="text-2xl font-bold tracking-tight text-white">Biblioteca de Cartas</h1>

            {/* Campo de BuscaCarta */}
            <input
                type="text"
                placeholder="Digite o nome da carta..."
                value={buscaCarta}
                onChange={(e) => setBuscaCarta(e.target.value)}
                className="mt-6 w-full max-w-sm rounded-lg border border-slate-700 bg-slate-800/80 px-4 py-2.5
                           text-slate-100 shadow-sm transition placeholder:text-slate-500
                           focus:border-red-500 focus:outline-none focus:ring-2 focus:ring-red-500/40"
            />

            {/* Dropdowns dos filtros */}
            <div className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-3">

                {/* Filtro de Classe */}
                <div>
                    <label className="mb-1.5 block text-sm font-medium text-slate-300">Classe:</label>
                    <select className={selectClasses} value={classeSelecionada} onChange={(e) => setClasseSelecionada(e.target.value)}>
                        <option value="">Todas</option>
                        {opcoesClasse.map(cls => <option key={cls} value={cls}>{cls}</option>)}
                    </select>
                </div>

                {/* Filtro de Tipo */}
                <div>
                    <label className="mb-1.5 block text-sm font-medium text-slate-300">Tipo:</label>
                    <select className={selectClasses} value={tipoSelecionado} onChange={(e) => setTipoSelecionado(e.target.value)}>
                        <option value="">Todas</option>
                        {opcoesTipos.map(t => <option key={t} value={t}>{t}</option>)}
                    </select>
                </div>

                {/* Filtro de Peças Necessárias */}
                <div>
                    <label className="mb-1.5 block text-sm font-medium text-slate-300">Peças Necessárias:</label>
                    <select className={selectClasses} value={pecaSelecionada} onChange={(e) => setPecaSelecionada(e.target.value)}>
                        <option value="">Todas</option>
                        {opcoesPecas.map(p => <option key={p} value={p}>{p}</option>)}
                    </select>
                </div>
            </div>

            <div className="mt-6 overflow-x-auto rounded-xl border border-slate-800 shadow-lg">
                <table className="w-full border-collapse bg-slate-900/60 text-sm">
                    <thead className="bg-slate-800/80">
                        <tr>
                            <th className={thClasses} onClick={() => handleSort('id')}>ID{renderSeta('id')}</th>
                            <th className={thClasses} onClick={() => handleSort('nome')}>Nome{renderSeta('nome')}</th>
                            <th className={thClasses} onClick={() => handleSort('class')}>Classe{renderSeta('class')}</th>
                            <th className={thClasses} onClick={() => handleSort('tipo_nome')}>Tipo{renderSeta('tipo_nome')}</th>
                            <th className="whitespace-nowrap px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-400">Descrição</th>
                            <th className={thClasses} onClick={() => handleSort('efeito_nome')}>Efeito{renderSeta('efeito_nome')}</th>
                            <th className={thClasses} onClick={() => handleSort('requisitos_pecas')}>Peças Necessárias{renderSeta('requisitos_pecas')}</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800">
                        {/* Usando a lista filtrada para o map */}
                        {cartasFiltradasEOrdenadas.map((carta) => (
                            <tr key={carta.id} className="transition hover:bg-slate-800/50">
                                <td className="whitespace-nowrap px-4 py-3 text-slate-300">{carta.id}</td>
                                <td className="whitespace-nowrap px-4 py-3 font-medium text-white">{carta.nome}</td>
                                <td className="whitespace-nowrap px-4 py-3 text-slate-300">{carta.class}</td>
                                <td className="whitespace-nowrap px-4 py-3 text-slate-300">{carta.tipo_nome}</td>
                                <td className="px-4 py-3 text-slate-400">{carta.descricao}</td>
                                <td className="whitespace-nowrap px-4 py-3 text-slate-300">{carta.efeito_nome}</td>
                                <td className="px-4 py-3 text-slate-300">
                                    {(carta.requisitos_pecas || []).length > 0
                                        ? carta.requisitos_pecas.join(", ")
                                    : "Vazio"}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {/* Aviso no caso de não ter resultados para retornar */}
            {cartasFiltradas.length === 0 && (
                <p className="mt-6 text-center text-slate-500">Nenhuma carta encontrada.</p>
            )}
        </div>
    );
}
