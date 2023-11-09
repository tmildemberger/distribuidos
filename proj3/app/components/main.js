import React from "react";
import {Link} from "react-router-dom";
const Main = () => {
  return (
    <div>
      <h3>Main</h3>
      <Link to="/entradaProduto" >Entrada de produto </Link>
      <Link to="/saidaProduto" >Saída de Produto</Link>
      <Link to="/relatorio" >Relatórios</Link>
    </div>
  );
};
export default Main;