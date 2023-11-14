import React, {useState, useReducer, useEffect} from "react";
import {useNavigate} from "react-router-dom";
import {Button, Stack, Container, Typography, TextField} from '@mui/material';
import toast from 'react-hot-toast';

const SaidaProduto = ({stub}) => {
    const navigate = useNavigate();

    const formReducer = (state, event) => {
      return {
        ...state,
        [event.name]: event.value
      };
    }
  
    const [formData, setFormData] = useReducer(formReducer, {
      codigo: '',
      quantidade: ''
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
        toast('Sucesso no lançamento de saída');
        navigate('/');
      }
    }
  
    const handleLancar = (e) => {
      console.log(formData);
      setFormReady(false);
      stub.LancarSaida(formData, lancamento_callback);
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
            Saída de Produto
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
          <Button variant="contained" onClick={handleLancar} disabled={!formReady}>Lançar Saída</Button>
          <Button variant="contained" onClick={handleVoltar} color="secondary">Voltar</Button>
        </Stack>
      </Container>
    );
};
export default SaidaProduto;