import React, {useState} from "react";
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
  const [formData, setFormData] = useState({
    produto_id: '',
    produto_nome: '',
    produto_desc: '',
    produto_preco: '',
    produto_estoque_qtd: '',
    produto_estoque_min: '',
  });

  const handleInputChange = (e) => {
    setFormData({
      data: e.target.value,
    });
  };

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    var argv = parseArgs(process.argv.slice(2), {
      string: 'target'
    });
    var target;
    if (argv.target) {
      target = argv.target;
    } else {
      target = 'localhost:50051';
    }
    const client = new my_proto.DadosEntrada.Greeter(target,
      grpc.credentials.createInsecure());

    client.DadosEntrada({codigo:formData.produto_id,
                        quantidade:formData.produto_estoque_qtd,
                        nome:formData.produto_nome,
                        descricao:formData.produto_desc,
                        preco_unitario:formData.produto_preco,
                        estoque_minimo:formData.produto_estoque_min}, function(err, response) {
                          console.log('Resposta Servidor:', response.message);
                        });
    // const client = new YourServiceClient('http://localhost:8080'); // Adjust the URL accordingly

    // const request = new DadosEntrada();

    // request.setID(formData.produto_id);
    // request.setNome(formData.produto_nome);
    // request.setQtd(formData.produto_estoque_qtd);
    // request.setDesc(formData.produto_desc);
    // request.setEstoque(formData.produto_estoque_min);
    // request.setPreco(formData.produto_preco);

    // try {
    //   const response = await client.DadosEntrada(request, {});
    //   console.log('Server response:', response.getResult());
    // } catch (error) {
    //   console.error('Error:', error);
    // }
  };
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
      <form onSubmit={handleFormSubmit}>
        <p>Código</p>
        <input name="Codigo" value = {formData.produto_id} onChange={handleInputChange}/>
        <p>Nome</p>
        <input name="Nome" value={formData.produto_nome} onChange={handleInputChange} />
        <p>Descrição</p>
        <input name="Descricao" value={formData.produto_desc} onChange={handleInputChange} />
        <p>Preço</p>
        <input name="Preco"  value={formData.produto_preco} onChange={handleInputChange} />
        <p>Quantidade em Estoque</p>
        <input name="Estoque" value={formData.produto_estoque_qtd} onChange={handleInputChange}/>
        <p>Estoque Mínimo</p>
        <input name="EstoqueMin" value={formData.produto_estoque_min} onChange={handleInputChange} />
        <br/>
        <button type='submit'>Submit</button>
</form>
    </div>
  );
};
export default EntradaProduto;