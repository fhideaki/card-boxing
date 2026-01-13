import React, { useState, useSyncExternalStore } from "react";

export default function Cards() {
    // Estado para armazenar o que o usuário digita
    const [buscaCarta, setBuscaCarta] = useState("");

    // Estados para os filtros
    const [classeSelecionada, setClasseSelecionada] = useState("");
    const [tipoSelecionado, setTipoSelecionado] = useState("");
    const [pecaSelecionada, setPecaSelecionada] = useState("");

    // Dados simulados das cartas
    const listaCartas = [
        {
            id: 1,
            nome: "Impacto de Sucata",
            classe: "Tanque",
            tipo: "Ataque",
            descricao: "Um golpe pesado usando restos metálicos.",
            efeito: "Causa 50 de dano físico.",
            requisitoPecas: ["Braço de Ferro", "Mola Hidráulica"]
        },
        {
            id: 2,
            nome: "Escudo de Plasma",
            classe: "Suporte",
            tipo: "Defesa",
            descricao: "Cria uma barreira de energia.",
            efeito: "Bloqueia 30 de dano no próximo turno.",
            requisitoPecas: [] // Vazio - sem requisito
        }
    ];
    
    // Criando as opções dos dropdowns de forma dinâmica
    // Usando o objeto Set para garantir que não ocorram repetições
    const opcoesClasse = [...new Set(listaCartas.map(c => c.classe))];
    const opcoesTipos = [...new Set(listaCartas.map(c => c.tipo))];
    // Para as peças, pode existir uma lista, então ela precisa ser achatada antes.
    const opcoesPecas = [...new Set(listaCartas.flatMap(c => c.requisitoPecas))]; 

    // Lógica para a filtragem combinada
    const cartasFiltradas = listaCartas.filter((carta) => {
        const bateNome = carta.nome.toLowerCase().includes(buscaCarta.toLowerCase());
        const bateClasse = classeSelecionada === "" || carta.classe === classeSelecionada;
        const bateTipo = tipoSelecionado === "" || carta.tipo === tipoSelecionado;
        const batePeca = pecaSelecionada === "" || carta.requisitoPecas.includes(pecaSelecionada);

        return bateNome && bateClasse && bateTipo && batePeca;
    });

    return (
        <div>
            <h1>Biblioteca de Cartas</h1>

            {/* Campo de BuscaCarta */}
            <input
                type="text"
                placeholder="Digite o nome da carta..."
                value={buscaCarta}
                onChange={(e) => setBuscaCarta(e.target.value)}
            />

            {/* Dropdowns dos filtros */}
            <div>

                {/* Filtro de Classe */}
                <div>
                    <label>Classe: </label>
                    <select value={classeSelecionada} onChange={(e) => setClasseSelecionada(e.target.value)}>
                        <option value="">Todas</option>
                        {opcoesClasse.map(cls => <option key={cls} value={cls}>{cls}</option>)}
                    </select>
                </div>

                {/* Filtro de Tipo */}
                <div>
                    <label>Tipo: </label>
                    <select value={tipoSelecionado} onChange={(e) => setTipoSelecionado(e.target.value)}>
                        <option value="">Todas</option>
                        {opcoesTipos.map(t => <option key={t} value={t}>{t}</option>)}
                    </select>
                </div>

                {/* Filtro de Peças Necessárias */}
                <div>
                    <label>Peças Necessárias: </label>
                    <select value={pecaSelecionada} onChange={(e) => setPecaSelecionada(e.target.value)}>
                        <option value="">Todas</option>
                        {opcoesPecas.map(p => <option key={p} value={p}>{p}</option>)}
                    </select>
                </div>
            </div>

            <table border="1">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nome</th>
                        <th>Classe</th>
                        <th>Tipo</th>
                        <th>Descrição</th>
                        <th>Efeito</th>
                        <th>Peças Necessárias</th>
                    </tr>
                </thead>
                <tbody>
                    {/* Usando a lista filtrada para o map */}
                    {cartasFiltradas.map((carta) => (
                        <tr key={carta.id}>
                            <td>{carta.id}</td>
                            <td>{carta.nome}</td>
                            <td>{carta.classe}</td>
                            <td>{carta.tipo}</td>
                            <td>{carta.descricao}</td>
                            <td>{carta.efeito}</td>
                            <td>
                                {carta.requisitoPecas.length > 0
                                    ? carta.requisitoPecas.join(", ")
                                : "Vazio"}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>

            {/* Aviso no caso de não ter resultados para retornar */}
            {cartasFiltradas.length === 0 && <p>Nenhuma carta encontrada.</p>}
        </div>
    );
}