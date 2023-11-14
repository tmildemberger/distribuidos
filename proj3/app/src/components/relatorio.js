import React, { useState } from "react";
import {Link} from "react-router-dom";
import Button from '@mui/material/Button';
import { TextField } from "@mui/material";
import InputMask from 'react-input-mask';

const Relatorio = () => {
  let [date1, setDate] = useState('');
  let [hora, setHora] = useState('');

  const relatorioProdutos = () => {
    console.log("Produtos em Estoque");
  };

  let relatorioMovimentacao = () => {
    console.log("Movimentacao ");
  };

  let relatorioProdSemSaida = () => {
    console.log("Produtos sem Saída ");
  };

  let handleDateChange = (e) => {
    setDate(e.target.value);
    console.log('A Data é:', e.target.value);
  };

  let handleHoraChange = (e) => {
    setHora(e.target.value);
  };

  return (
    <div>
      <h3>Relatorio</h3>
      <Link to="/entradaProduto" >Entrada de produto </Link>
      <Link to="/saidaProduto" >Saída de Produto</Link>
      <Link to="/relatorio" >Relatórios</Link>

      <p>Período de Tempo</p><TextField label="Data" value={date1} onChange={handleDateChange}><InputMask mask="00/00/00" maskChar="/" /></TextField><TextField label="Horário" value={hora} onChange={handleHoraChange}><InputMask mask="00:00:00" maskChar=":" /></TextField>
      <br/>
      <br/>
      <Button variant='contained' onClick={relatorioProdutos}>Produtos em Estoque</Button>
      <Button variant='contained' onClick={relatorioMovimentacao}>Relatório de Movimentações</Button>
      <Button variant='contained' onClick={relatorioProdSemSaida}>Relatório de Produtos sem Saída</Button>
    </div>
  );
};
export default Relatorio;