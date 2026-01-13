import React, { useState } from "react";
import { Link } from "react-router-dom";

export default function Navbar() {

    // Estado para controlar a visibilidade do pop-up
    const [isModalOpen, setIsModalOpen] = useState(false);

    // Estados para os campos do formulário
    const [usuario, setUsuario] = useState("");
    const [senha, setSenha] = useState("");

    // Funções para os botões
    const handleLogin = () => {
        console.log("Tentando login com:", usuario, senha);
        // Inserir a lógica de validação no futuro
    };

    const handleCadastro = () => {
        console.log("Executando lógica de cadastro com: ", usuario);
    };

    return (
        <nav className="navbar-container">
            <div className="logo">
                <Link to="/">Robot Card Boxing</Link>
            </div>

            <ul className="nav-links">
                <li><Link to="/cards">Cartas</Link></li>
                <li><Link to="/parts">Partes</Link></li>
                <li><Link to="/robots">Meus Robôs</Link></li>
                <li>
                    <button 
                        onClick={() => setIsModalOpen(true)}
                        style={{ background: 'none', border: 'none', cursor:'pointer', color:'inherit', font:'inherit' }}
                    >
                        Login
                    </button>

                    {isModalOpen && (
                        <div className="modal-overlay">
                            <div className="modal-content">
                                <h3>Login</h3>

                                <label>Usuário:</label>
                                <input 
                                    type="text"
                                    value={usuario}
                                    onChange={(e) => setUsuario(e.target.value)}
                                />

                                <label>Senha:</label>
                                <input 
                                    type="password"
                                    value={senha}
                                    onChange={(e) => setSenha(e.target.value)}
                                />

                                <div className="modal-buttons">
                                    <button onClick={handleLogin}>Login</button>
                                    <button onClick={handleCadastro}>Cadastre-se</button>
                                    <button onClick={() => setIsModalOpen(false)}>Cancelar </button>
                                </div>
                                
                            </div>
                        </div>
                    )}
                </li>
            </ul>
        </nav>
    )
}