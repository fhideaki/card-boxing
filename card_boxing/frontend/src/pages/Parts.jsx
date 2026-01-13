import React, { useState, useSyncExternalStore } from "react";

export default function Parts() {
    // Estado para armazenar o que o usuário digita
    const [buscaPeca, setBuscaPeca] = useState("");

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
            // Peça que não libera carta ou libera sozinha
            liberaCartas: [
                { carta: "Recarregar", precisaDe: null }
            ]
        },
        {
            id: 2,
            nome: "Lançador de Chamas",
            slot: "Braço",
            tipo: "Fogo",
            conmod: 0,
            strmod: 8,
            agimod: -2,
            hpmod: 0,
            fraquezas: ["Gelo"],
            resistencias: ["Fogo"],
            // Precisa do Tanque de Combustível para a carta especial
            liberaCartas: [
                { carta: "Chama Constante", precisaDe: null },
                { carta: "Explosão de Nafta", precisaDe: "Tanque de Combustível" }
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
            // Precisa do Lançador de Chamas para a mesma carta
            liberaCartas: [
                { carta: "Explosão de Nafta", precisaDe: "Lançador de Chamas" }
            ]
        }
    ];
    
    // Criando as opções dos dropdowns de forma dinâmica
    // Usando o objeto Set para garantir que não ocorram repetições
    const opcoesSlots = [...new Set(listaPecas.map(p => p.slot))];
    const opcoesTipos = [...new Set(listaPecas.map(p => p.tipo))];
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
        const bateTipo = tipoSelecionado === "" || peca.tipo === tipoSelecionado;
        const bateFraqueza = tipoFraquezaSelecionado === "" || peca.fraquezas.includes(tipoFraquezaSelecionado);
        const bateResistencia = tipoResistenciaSelecionado === "" || peca.resistencias.includes(tipoResistenciaSelecionado);
        const bateCarta = cartaSelecionada === "" || peca.liberaCartas.some(item => item.carta === cartaSelecionada);
        const bateConMod = conModSelecionado === "" || peca.conmod === conModSelecionado;
        const bateStrMod = strModSelecionado === "" || peca.strmod === strModSelecionado;
        const bateAgiMod = agiModSelecionado === "" || peca.agimod === agiModSelecionado;
        const bateHpMod = hpModSelecionado === "" || peca.hpmod === hpModSelecionado;

        console.log(`Peça: ${peca.nome} | Bate Slot: ${bateSlot} | Bate Tipo: ${bateTipo}`);
        return bateNome && bateSlot && bateTipo && bateFraqueza && bateResistencia && bateCarta && bateConMod && bateStrMod && bateAgiMod && bateHpMod;
    });

    return (
        <div>
            <h1>Biblioteca de Peças</h1>

            {/* Campo de BuscaPeca */}
            <input
                type="text"
                placeholder="Digite o nome da peça..."
                value={buscaPeca}
                onChange={(e) => setBuscaPeca(e.target.value)}
            />

            {/* Dropdowns dos filtros */}
            <div>

                {/* Filtro de Slot */}
                <div>
                    <label>Slot: </label>
                    <select value={slotSelecionado} onChange={(e) => setSlotSelecionado(e.target.value)}>
                        <option value="">Todos</option>
                        {opcoesSlots.map(s => <option key={s} value={s}>{s}</option>)}
                    </select>
                </div>

                {/* Filtro de Tipo */}
                <div>
                    <label>Tipo: </label>
                    <select value={tipoSelecionado} onChange={(e) => setTipoSelecionado(e.target.value)}>
                        <option value="">Todos</option>
                        {opcoesTipos.map(t => <option key={t} value={t}>{t}</option>)}
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

                {/* Filtro de Cartas */}
                <div>
                    <label>Cartas: </label>
                    <select value={cartaSelecionada} onChange={(e) => setCartaSelecionada(e.target.value)}>
                        <option value="">Todas</option>
                        {opcoesCartas.map(c => <option key={c} value={c}>{c}</option>)}
                    </select>
                </div>

                {/* Filtro de Modificador de Constituição */}
                <div>
                    <label>Constituição: </label>
                    <select value={conModSelecionado} onChange={(e) => setConModSelecionado(e.target.value)}>
                        <option value="">Todos</option>
                        {opcoesConMod.map(cm => <option key={cm} value={cm}>{cm}</option>)}
                    </select>
                </div>                
                
                {/* Filtro de Modificador de Força */}
                <div>
                    <label>Força: </label>
                    <select value={strModSelecionado} onChange={(e) => setStrModSelecionado(e.target.value)}>
                        <option value="">Todos</option>
                        {opcoesStrMod.map(sm => <option key={sm} value={sm}>{sm}</option>)}
                    </select>
                </div>

                {/* Filtro de Modificador de Agilidade */}
                <div>
                    <label>Agilidade: </label>
                    <select value={agiModSelecionado} onChange={(e) => setAgiModSelecionado(e.target.value)}>
                        <option value="">Todos</option>
                        {opcoesAgiMod.map(am => <option key={am} value={am}>{am}</option>)}
                    </select>
                </div>

                {/* Filtro de Modificador de HP */}
                <div>
                    <label>HP: </label>
                    <select value={hpModSelecionado} onChange={(e) => setHpModSelecionado(e.target.value)}>
                        <option value="">Todos</option>
                        {opcoesHpMod.map(hm => <option key={hm} value={hm}>{hm}</option>)}
                    </select>
                </div>
            </div>

            <table border="1">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nome</th>
                        <th>Slot</th>
                        <th>Tipo</th>
                        <th>Fraquezas</th>
                        <th>Resistências</th>
                        <th>Constituição</th>
                        <th>Força</th>
                        <th>Agilidade</th>
                        <th>HP</th>
                        <th>Cartas</th>
                    </tr>
                </thead>
                <tbody>
                    {/* Usando a lista filtrada para o map */}
                    {pecasFiltradas.map((peca) => (
                        <tr key={peca.id}>
                            <td>{peca.id}</td>
                            <td>{peca.nome}</td>
                            <td>{peca.slot}</td>
                            <td>{peca.tipo}</td>
                            <td>{peca.fraquezas}</td>
                            <td>{peca.resistencias}</td>
                            <td>{peca.conmod}</td>
                            <td>{peca.strmod}</td>
                            <td>{peca.agimod}</td>
                            <td>{peca.hpmod}</td>
                            <td>
                                {peca.liberaCartas.map((item, index) => (
                                    <div key={index}>
                                        <strong>{item.carta}</strong>
                                        {item.precisaDe ? ` (Requer: ${item.precisaDe})` : " (Individual)"}
                                    </div>
                                ))}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>

            {/* Aviso no caso de não ter resultados para retornar */}
            {pecasFiltradas.length === 0 && <p>Nenhuma peça encontrada.</p>}
        </div>
    );
}