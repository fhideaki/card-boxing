import React, { useEffect, useState, useSyncExternalStore } from "react";

export default function Parts() {
    // Estado para armazenar o que o usuário digita
    const [buscaPeca, setBuscaPeca] = useState("");

    // Estado para armazenar a ordenação da tabela
    const [ordenacao, setOrdenacao] = useState({ coluna: null, direcao: null });

    // Estados para os filtros
    const [slotSelecionado, setSlotSelecionado] = useState("");
    const [tipoSelecionado, setTipoSelecionado] = useState("");
    const [tipoFraquezaSelecionado, setTipoFraquezaSelecionado] = useState("");
    const [tipoResistenciaSelecionado, setTipoResistenciaSelecionado] = useState("");
    const [cartaSelecionada, setCartaSelecionada] = useState("");
    const [conModSelecionado, setConModSelecionado] = useState("");
    const [strModSelecionado, setStrModSelecionado] = useState("");
    const [agiModSelecionado, setAgiModSelecionado] = useState("");
    const [hpModSelecionado, setHpModSelecionado] = useState("");

    // Dados simulados das cartas
    const [listaPecas, setListaPecas] = useState([]);

    useEffect(() => {
        const carregarPecas = async () => {
            try {
                const resposta = await fetch('http://127.0.0.1:5000/api/parts');
                const dados = await resposta.json();
                setListaPecas(dados);
            } catch (erro) {
                console.error("Erro ao buscar peças:", erro);
            }
        };

        carregarPecas();
    }, []);

    // Criando as opções dos dropdowns de forma dinâmica
    // Usando o objeto Set para garantir que não ocorram repetições
    const opcoesSlots = [...new Set(listaPecas.map(p => p.slot))];
    const opcoesTipos = [...new Set(listaPecas.map(p => p.tipo_nome))];
    // Para as fraquezas, resistências e cartas, pode existir uma lista, então ela precisa ser achatada antes.
    const opcoesFraquezas = [...new Set(listaPecas.flatMap(p => p.fraquezas))];
    const opcoesResistencias = [...new Set(listaPecas.flatMap(p => p.resistencias))];
    const opcoesCartas = [...new Set(listaPecas.flatMap(p => p.liberaCartas.map(c => c.carta)))];
    const opcoesConMod = [...new Set(listaPecas.map(p => p.conmod))];
    const opcoesStrMod = [...new Set(listaPecas.map(p => p.strmod))];
    const opcoesAgiMod = [...new Set(listaPecas.map(p => p.agimod))];
    const opcoesHpMod = [...new Set(listaPecas.map(p => p.hpmod))];

    // Lógica para a filtragem combinada
    const pecasFiltradas = listaPecas.filter((peca) => {
        const bateNome = peca.nome.toLowerCase().includes(buscaPeca.toLowerCase());
        const bateSlot = slotSelecionado === "" || peca.slot === slotSelecionado;
        const bateTipo = tipoSelecionado === "" || peca.tipo_nome === tipoSelecionado;
        const bateFraqueza = tipoFraquezaSelecionado === "" || peca.fraquezas.includes(tipoFraquezaSelecionado);
        const bateResistencia = tipoResistenciaSelecionado === "" || peca.resistencias.includes(tipoResistenciaSelecionado);
        const bateCarta = cartaSelecionada === "" || peca.liberaCartas.some(item => item.carta === cartaSelecionada);
        const bateConMod = conModSelecionado === "" || peca.conmod === Number(conModSelecionado);
        const bateStrMod = strModSelecionado === "" || peca.strmod === Number(strModSelecionado);
        const bateAgiMod = agiModSelecionado === "" || peca.agimod === Number(agiModSelecionado);
        const bateHpMod = hpModSelecionado === "" || peca.hpmod === Number(hpModSelecionado);

        console.log(`Peça: ${peca.nome} | Bate Slot: ${bateSlot} | Bate Tipo: ${bateTipo}`);
        return bateNome && bateSlot && bateTipo && bateFraqueza && bateResistencia && bateCarta && bateConMod && bateStrMod && bateAgiMod && bateHpMod;
    });

    // Lógica para ordenar a filtragem
    const pecasFiltradasEOrdenadas = [...pecasFiltradas].sort((a, b) => {
        if (!ordenacao.coluna || !ordenacao.direcao) return 0;

        const valorA = a[ordenacao.coluna];
        const valorB = b[ordenacao.coluna];

        if (valorA < valorB) return ordenacao.direcao === 'asc' ? -1 : 1;
        if (valorA > valorB) return ordenacao.direcao === 'asc' ? 1: -1;
        return 0;
    });

    // Criando o componente de cabeçalho para ordenação
    const handleSort = (coluna) => {
        setOrdenacao(prev => {
            if (prev.coluna !== coluna) return { coluna, direcao: 'asc' };
            if (prev.direcao === 'asc') return { coluna, direcao: 'desc' };
            return { coluna: null, direcao: null } // Isso é para zerar o filtro
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
        <div className="mx-auto max-w-7xl px-6 py-10">
            <h1 className="text-2xl font-bold tracking-tight text-white">Biblioteca de Peças</h1>

            {/* Campo de BuscaPeca */}
            <input
                type="text"
                placeholder="Digite o nome da peça..."
                value={buscaPeca}
                onChange={(e) => setBuscaPeca(e.target.value)}
                className="mt-6 w-full max-w-sm rounded-lg border border-slate-700 bg-slate-800/80 px-4 py-2.5
                           text-slate-100 shadow-sm transition placeholder:text-slate-500
                           focus:border-red-500 focus:outline-none focus:ring-2 focus:ring-red-500/40"
            />

            {/* Dropdowns dos filtros */}
            <div className="mt-4 grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-5">

                {/* Filtro de Slot */}
                <div>
                    <label className="mb-1.5 block text-sm font-medium text-slate-300">Slot:</label>
                    <select className={selectClasses} value={slotSelecionado} onChange={(e) => setSlotSelecionado(e.target.value)}>
                        <option value="">Todos</option>
                        {opcoesSlots.map(s => <option key={s} value={s}>{s}</option>)}
                    </select>
                </div>

                {/* Filtro de Tipo */}
                <div>
                    <label className="mb-1.5 block text-sm font-medium text-slate-300">Tipo:</label>
                    <select className={selectClasses} value={tipoSelecionado} onChange={(e) => setTipoSelecionado(e.target.value)}>
                        <option value="">Todos</option>
                        {opcoesTipos.map(t => <option key={t} value={t}>{t}</option>)}
                    </select>
                </div>

                {/* Filtro de Fraquezas */}
                <div>
                    <label className="mb-1.5 block text-sm font-medium text-slate-300">Fraquezas:</label>
                    <select className={selectClasses} value={tipoFraquezaSelecionado} onChange={(e) => setTipoFraquezaSelecionado(e.target.value)}>
                        <option value="">Todas</option>
                        {opcoesFraquezas.map(f => <option key={f} value={f}>{f}</option>)}
                    </select>
                </div>

                {/* Filtro de Resistências */}
                <div>
                    <label className="mb-1.5 block text-sm font-medium text-slate-300">Resistências:</label>
                    <select className={selectClasses} value={tipoResistenciaSelecionado} onChange={(e) => setTipoResistenciaSelecionado(e.target.value)}>
                        <option value="">Todas</option>
                        {opcoesResistencias.map(r => <option key={r} value={r}>{r}</option>)}
                    </select>
                </div>

                {/* Filtro de Cartas */}
                <div>
                    <label className="mb-1.5 block text-sm font-medium text-slate-300">Cartas:</label>
                    <select className={selectClasses} value={cartaSelecionada} onChange={(e) => setCartaSelecionada(e.target.value)}>
                        <option value="">Todas</option>
                        {opcoesCartas.map(c => <option key={c} value={c}>{c}</option>)}
                    </select>
                </div>

                {/* Filtro de Modificador de Constituição */}
                <div>
                    <label className="mb-1.5 block text-sm font-medium text-slate-300">Constituição:</label>
                    <select className={selectClasses} value={conModSelecionado} onChange={(e) => setConModSelecionado(e.target.value)}>
                        <option value="">Todos</option>
                        {opcoesConMod.map(cm => <option key={cm} value={cm}>{cm}</option>)}
                    </select>
                </div>

                {/* Filtro de Modificador de Força */}
                <div>
                    <label className="mb-1.5 block text-sm font-medium text-slate-300">Força:</label>
                    <select className={selectClasses} value={strModSelecionado} onChange={(e) => setStrModSelecionado(e.target.value)}>
                        <option value="">Todos</option>
                        {opcoesStrMod.map(sm => <option key={sm} value={sm}>{sm}</option>)}
                    </select>
                </div>

                {/* Filtro de Modificador de Agilidade */}
                <div>
                    <label className="mb-1.5 block text-sm font-medium text-slate-300">Agilidade:</label>
                    <select className={selectClasses} value={agiModSelecionado} onChange={(e) => setAgiModSelecionado(e.target.value)}>
                        <option value="">Todos</option>
                        {opcoesAgiMod.map(am => <option key={am} value={am}>{am}</option>)}
                    </select>
                </div>

                {/* Filtro de Modificador de HP */}
                <div>
                    <label className="mb-1.5 block text-sm font-medium text-slate-300">HP:</label>
                    <select className={selectClasses} value={hpModSelecionado} onChange={(e) => setHpModSelecionado(e.target.value)}>
                        <option value="">Todos</option>
                        {opcoesHpMod.map(hm => <option key={hm} value={hm}>{hm}</option>)}
                    </select>
                </div>
            </div>

            <div className="mt-6 overflow-x-auto rounded-xl border border-slate-800 shadow-lg">
                <table className="w-full border-collapse bg-slate-900/60 text-sm">
                    <thead className="bg-slate-800/80">
                        <tr>
                            <th className={thClasses} onClick={() => handleSort('id')}>ID{renderSeta('id')}</th>
                            <th className={thClasses} onClick={() => handleSort('nome')}>Nome{renderSeta('nome')}</th>
                            <th className={thClasses} onClick={() => handleSort('slot')}>Slot{renderSeta('slot')}</th>
                            <th className={thClasses} onClick={() => handleSort('tipo_nome')}>Tipo{renderSeta('tipo_nome')}</th>
                            <th className={thClasses} onClick={() => handleSort('fraquezas')}>Fraquezas{renderSeta('fraquezas')}</th>
                            <th className={thClasses} onClick={() => handleSort('resistencias')}>Resistências{renderSeta('resistencias')}</th>
                            <th className={thClasses} onClick={() => handleSort('conmod')}>Constituição{renderSeta('conmod')}</th>
                            <th className={thClasses} onClick={() => handleSort('strmod')}>Força{renderSeta('strmod')}</th>
                            <th className={thClasses} onClick={() => handleSort('agimod')}>Agilidade{renderSeta('agimod')}</th>
                            <th className={thClasses} onClick={() => handleSort('hpmod')}>HP{renderSeta('hpmod')}</th>
                            <th className={thClasses} onClick={() => handleSort('carta')}>Cartas{renderSeta('carta')}</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800">
                        {/* Usando a lista filtrada para o map */}
                        {pecasFiltradasEOrdenadas.map((peca) => (
                            <tr key={peca.id} className="transition hover:bg-slate-800/50">
                                <td className="whitespace-nowrap px-4 py-3 text-slate-300">{peca.id}</td>
                                <td className="whitespace-nowrap px-4 py-3 font-medium text-white">{peca.nome}</td>
                                <td className="whitespace-nowrap px-4 py-3 text-slate-300">{peca.slot}</td>
                                <td className="whitespace-nowrap px-4 py-3 text-slate-300">{peca.tipo_nome}</td>
                                <td className="whitespace-nowrap px-4 py-3 text-slate-300">{peca.fraquezas.join(', ')}</td>
                                <td className="whitespace-nowrap px-4 py-3 text-slate-300">{peca.resistencias.join(', ')}</td>
                                <td className="whitespace-nowrap px-4 py-3 text-slate-300">{peca.conmod}</td>
                                <td className="whitespace-nowrap px-4 py-3 text-slate-300">{peca.strmod}</td>
                                <td className="whitespace-nowrap px-4 py-3 text-slate-300">{peca.agimod}</td>
                                <td className="whitespace-nowrap px-4 py-3 text-slate-300">{peca.hpmod}</td>
                                <td className="px-4 py-3 text-slate-300">
                                    {peca.liberaCartas.map((item, index) => (
                                        <div key={index}>
                                            <strong className="text-white">{item.carta}</strong>
                                            {item.precisaDe ? ` (Requer: ${item.precisaDe})` : " (Individual)"}
                                        </div>
                                    ))}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {/* Aviso no caso de não ter resultados para retornar */}
            {pecasFiltradas.length === 0 && (
                <p className="mt-6 text-center text-slate-500">Nenhuma peça encontrada.</p>
            )}
        </div>
    );
}
