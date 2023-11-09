import React from "react";
import {Link} from "react-router-dom";
const SaidaProduto = () => {
  return (
    <div>
      <h3>Saida de Produto</h3>
      <Link to="/entradaProduto" >Entrada de produto </Link>
      <br/>
      <Link to="/saidaProduto" >Saída de Produto</Link>
      <br/>
      <Link to="/relatorio" >Relatórios</Link>
      <br/>
      <form>
        <p>Código</p>
        <input name="Codigo" />
        <p>Quantidade</p>
        <input name="Estoque" />
        <br/>
        <button>Ok</button>
</form>
    </div>
  );
};
export default SaidaProduto;