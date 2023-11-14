import React from "react";
import {useNavigate} from "react-router-dom";
import {Button, Stack, Container, Typography} from '@mui/material';
import toast from 'react-hot-toast';
// import stub from './gestor_de_estoque_stub';

const Main = () => {
  const navigate = useNavigate();
  function handleEntrada(e) {
    navigate('/entradaProduto');
  }
  function handleSaida(e) {
    navigate('/saidaProduto');
  }
  function handleRelatorio(e) {
    navigate('/relatorio');
  }

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
          Gestor de Estoque
        </Typography>
        <Button variant="contained" onClick={handleEntrada}>Lançar Entrada</Button>
        <Button variant="contained" onClick={handleSaida}>Lançar Saída</Button>
        <Button variant="contained" onClick={handleRelatorio}>Gerar Relatórios</Button>
      </Stack>
    </Container>
  );
};
export default Main;