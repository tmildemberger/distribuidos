import logo from './logo.svg';
import './App.css';
import {BrowserRouter as Router, Routes, Route, Link} from "react-router-dom";

import Main from './components/main'; 
import EntradaProduto from './components/entradaProduto'; 
import SaidaProduto from './components/saidaProduto';
import Relatorio from './components/relatorio';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
      <Router>
        <Routes>
          <Route path="/" element={<Main/>} />
          <Route path="/entradaProduto" element={<EntradaProduto/>} />
          <Route path="/saidaProduto" element={<SaidaProduto/>} />
          <Route path="/relatorio" element={<Relatorio/>} />

        </Routes>
      </Router>
      
    </div>
  );
}

export default App;
