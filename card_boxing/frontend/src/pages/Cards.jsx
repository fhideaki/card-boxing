import React, { useEffect, useState, useSyncExternalStore } from "react";

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
                        <th onClick={() => handleSort('id')} style={{cursor: 'pointer'}}>ID {renderSeta('id')}</th>
                        <th onClick={() => handleSort('nome')} style={{cursor: 'pointer'}}>Nome {renderSeta('nome')}</th>
                        <th onClick={() => handleSort('class')} style={{cursor: 'pointer'}}>Classe {renderSeta('class')}</th>
                        <th onClick={() => handleSort('tipo_nome')} style={{cursor: 'pointer'}}>Tipo {renderSeta('tipo_nome')}</th>
                        <th>Descrição</th>
                        <th onClick={() => handleSort('efeito_nome')} style={{cursor: 'pointer'}}>Efeito {renderSeta('efeito_nome')}</th>
                        <th onClick={() => handleSort('requisitos_pecas')} style={{cursor: 'pointer'}}>Peças Necessárias {renderSeta('requisitos_pecas')}</th>
                    </tr>
                </thead>
                <tbody>
                    {/* Usando a lista filtrada para o map */}
                    {cartasFiltradasEOrdenadas.map((carta) => (
                        <tr key={carta.id}>
                            <td>{carta.id}</td>
                            <td>{carta.nome}</td>
                            <td>{carta.class}</td>
                            <td>{carta.tipo_nome}</td>
                            <td>{carta.descricao}</td>
                            <td>{carta.efeito_nome}</td>
                            <td>
                                {(carta.requisitos_pecas || []).length > 0
                                    ? carta.requisitos_pecas.join(", ")
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