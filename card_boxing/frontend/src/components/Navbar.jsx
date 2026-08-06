import React, { useState } from "react";
import { Link, useLocation } from "react-router-dom";

const links = [
    { to: "/cards", label: "Cartas" },
    { to: "/parts", label: "Partes" },
    { to: "/robots", label: "Meus Robôs" },
    { to: "/battle", label: "Batalha" },
];

export default function Navbar() {

    // Estado para controlar a visibilidade do pop-up
    const [isModalOpen, setIsModalOpen] = useState(false);

    // Estados para os campos do formulário
    const [usuario, setUsuario] = useState("");
    const [senha, setSenha] = useState("");

    const { pathname } = useLocation();

    // Funções para os botões
    const handleLogin = () => {
        console.log("Tentando login com:", usuario, senha);
        // Inserir a lógica de validação no futuro
    };

    const handleCadastro = () => {
        console.log("Executando lógica de cadastro com: ", usuario);
    };

    const inputClasses =
        "w-full rounded-lg border border-slate-700 bg-slate-800/80 px-4 py-2.5 text-slate-100 " +
        "shadow-sm transition focus:border-red-500 focus:outline-none focus:ring-2 focus:ring-red-500/40";

    return (
        <nav className="sticky top-0 z-50 border-b border-slate-800 bg-slate-950/90 backdrop-blur">
            <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-6">
                <Link to="/" className="text-lg font-extrabold tracking-tight text-white">
                    Robot <span className="text-red-500">Card Boxing</span>
                </Link>

                <ul className="flex items-center gap-1">
                    {links.map(({ to, label }) => (
                        <li key={to}>
                            <Link
                                to={to}
                                className={
                                    "rounded-md px-3 py-2 text-sm font-medium transition " +
                                    (pathname === to
                                        ? "bg-slate-800 text-white"
                                        : "text-slate-400 hover:bg-slate-800/60 hover:text-white")
                                }
                            >
                                {label}
                            </Link>
                        </li>
                    ))}
                    <li className="ml-2">
                        <button
                            onClick={() => setIsModalOpen(true)}
                            className="rounded-md bg-red-600 px-4 py-2 text-sm font-semibold text-white
                                       shadow-sm shadow-red-600/30 transition hover:bg-red-500"
                        >
                            Login
                        </button>

                        {isModalOpen && (
                            <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 px-4">
                                <div className="w-full max-w-sm rounded-2xl border border-slate-800 bg-slate-900 p-6 text-left shadow-2xl">
                                    <h3 className="mb-5 text-center text-xl font-bold text-white">Login</h3>

                                    <div className="space-y-4">
                                        <div>
                                            <label className="mb-1.5 block text-sm font-medium text-slate-300">Usuário:</label>
                                            <input
                                                type="text"
                                                value={usuario}
                                                onChange={(e) => setUsuario(e.target.value)}
                                                className={inputClasses}
                                            />
                                        </div>

                                        <div>
                                            <label className="mb-1.5 block text-sm font-medium text-slate-300">Senha:</label>
                                            <input
                                                type="password"
                                                value={senha}
                                                onChange={(e) => setSenha(e.target.value)}
                                                className={inputClasses}
                                            />
                                        </div>
                                    </div>

                                    <div className="mt-6 flex flex-col gap-2">
                                        <button
                                            onClick={handleLogin}
                                            className="w-full rounded-lg bg-gradient-to-r from-red-600 to-red-500 py-2.5 font-semibold
                                                       text-white shadow-md shadow-red-600/30 transition hover:from-red-500 hover:to-red-400"
                                        >
                                            Login
                                        </button>
                                        <button
                                            onClick={handleCadastro}
                                            className="w-full rounded-lg border border-slate-700 bg-slate-800 py-2.5 font-semibold
                                                       text-slate-200 transition hover:bg-slate-700"
                                        >
                                            Cadastre-se
                                        </button>
                                        <button
                                            onClick={() => setIsModalOpen(false)}
                                            className="w-full py-2 text-sm font-medium text-slate-400 transition hover:text-slate-200"
                                        >
                                            Cancelar
                                        </button>
                                    </div>
                                </div>
                            </div>
                        )}
                    </li>
                </ul>
            </div>
        </nav>
    )
}
