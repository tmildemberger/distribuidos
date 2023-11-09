import React from "react";
import {Link} from "react-router-dom";

var PROTO_PATH = __dirname + '/../../protos/helloworld.proto';

var parseArgs = require('minimist');
var grpc = require('@grpc/grpc-js');
var protoLoader = require('@grpc/proto-loader');
var packageDefinition = protoLoader.loadSync(
    PROTO_PATH,
    {keepCase: true,
     longs: String,
     enums: String,
     defaults: true,
     oneofs: true
    });
var my_proto = grpc.loadPackageDefinition(packageDefinition).helloworld;

const search = () => {
  console.log("Teste");
}

const EntradaProduto = () => {
  return (
    <div>
      <h3>Entrada de Produto</h3>
      <br/>
      <Link to="/entradaProduto" >Entrada de produto </Link>
      <br/>
      <Link to="/saidaProduto" >Saída de Produto</Link>
      <br/>
      <Link to="/relatorio" >Relatórios</Link>
      <br/>
      <form>
        <p>Código</p>
        <input name="Codigo" />
        <p>Nome</p>
        <input name="Nome" />
        <p>Descrição</p>
        <input name="Descricao" />
        <p>Preço</p>
        <input name="Preco" />
        <p>Estoque</p>
        <input name="Estoque" />
        <p>Estoque Mínimo</p>
        <input name="EstoqueMin" />
        <br/>
        <button>Ok</button>
</form>
    </div>
  );
};
export default EntradaProduto;