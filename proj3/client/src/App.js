import logo from './logo.svg';
import './App.css';
import toast, { Toaster } from 'react-hot-toast';
import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Main from './components/main'; 
import EntradaProduto from './components/entradaProduto'; 
import SaidaProduto from './components/saidaProduto';
import Relatorio from './components/relatorio';
import stub from './gestor_de_estoque_stub';

function App() {
  const BaseURL = "http://localhost:5000";

  useEffect(() => {
    const source = new EventSource(`${BaseURL}/stream`);

    source.addEventListener('open', () => {
      console.log('SSE aberto!');
    });

    source.addEventListener('message', (e) => {
      const data = JSON.parse(e.data);

      console.log("Notificação recebida");
      console.log(data);
      toast(data.mensagem, {
        duration: 10000,
        style: {
          borderRadius: '10px',
          background: '#333',
          color: '#fff',
        },
      });
    });

    source.addEventListener('error', (e) => {
      console.error('Erro: ', e);
    });

    return () => {
      source.close();
    };
  }, []);

  return (
    <div className="App">
      <Toaster
        position="top-right"
        reverseOrder={true}
      />
      <header>
        <img src={logo} className="App-logo" alt="logo" />
        <Router>
          <Routes>
            <Route path="/" element={<Main/>} />
            <Route path="/entradaProduto" element={<EntradaProduto stub={stub}/>} />
            <Route path="/saidaProduto" element={<SaidaProduto stub={stub}/>} />
            <Route path="/relatorio" element={<Relatorio stub={stub}/>} />

          </Routes>
        </Router>
      </header>
    </div>
  );
}

export default App;
