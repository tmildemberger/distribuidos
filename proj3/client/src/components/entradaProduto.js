import React, {useState, useReducer, useEffect} from "react";
import {useNavigate} from "react-router-dom";
import {Button, Stack, Container, Typography, TextField} from '@mui/material';
import toast from 'react-hot-toast';

const EntradaProduto = ({stub}) => {
  const navigate = useNavigate();

  const formReducer = (state, event) => {
    return {
      ...state,
      [event.name]: event.value
    };
  }

  const [formData, setFormData] = useReducer(formReducer, {
    codigo: '',
    quantidade: '',
    nome: '',
    descricao: '',
    preco_unitario: '',
    estoque_minimo: '',
  });

  const [formReady, setFormReady] = useState(false);

  const handleInputChange = (event) => {
    let val = event.target.value;
    if (event.target.type === 'number') {
      val = Number(event.target.value);
    }
    setFormData({
      name: event.target.name,
      value: val
    });
  }

  useEffect(() => {
    console.log(formData);
    let ok = true;
    for (const field in formData) {
      if (formData[field] === '') ok = false;
    }
    setFormReady(ok);
  }, [formData]);

  function lancamento_callback(error, estadoResposta) {
    console.log(error);
    console.log(estadoResposta);
    if (error) {
      return;
    }
    if (estadoResposta.estado === 'ok') {
      toast('Sucesso no lançamento de entrada');
      navigate('/');
    }
  }

  const handleLancar = (e) => {
    console.log(formData);
    setFormReady(false);
    stub.LancarEntrada(formData, lancamento_callback);
  };
  const handleVoltar = (e) => {
    navigate('/');
  };
  
  return (
    <Container>
      <Stack
        spacing={2}
        direction="column"
        justifyContent="center"
        alignItems="center"
        display="flex" 
        flexDirection="column"
      >
        <Typography variant="h4" gutterBottom>
          Entrada de Produto
        </Typography>
        <TextField
          label="Código"
          size="small"
          name="codigo"
          value={formData.codigo}
          onChange={handleInputChange}
          autoComplete="off"
        />
        <TextField
          label="Quantidade"
          size="small"
          name="quantidade"
          type="number"
          value={formData.quantidade}
          onChange={handleInputChange}
          autoComplete="off"
        />
        <TextField
          label="Nome"
          size="small"
          name="nome"
          value={formData.nome}
          onChange={handleInputChange}
          autoComplete="off"
        />
        <TextField
          label="Descrição"
          size="small"
          name="descricao"
          value={formData.descricao}
          onChange={handleInputChange}
          autoComplete="off"
        />
        <TextField
          label="Preço"
          size="small"
          name="preco_unitario"
          type="number"
          value={formData.preco_unitario}
          onChange={handleInputChange}
          autoComplete="off"
        />
        <TextField
          label="Estoque Mínimo"
          size="small"
          name="estoque_minimo"
          type="number"
          value={formData.estoque_minimo}
          onChange={handleInputChange}
          autoComplete="off"
        />
        <Button variant="contained" onClick={handleLancar} disabled={!formReady}>Lançar Entrada</Button>
        <Button variant="contained" onClick={handleVoltar} color="secondary">Voltar</Button>
      </Stack>
    </Container>
  );
};
export default EntradaProduto;