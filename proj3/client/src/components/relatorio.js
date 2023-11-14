import React, {useState, useReducer, useEffect} from "react";
import {useNavigate} from "react-router-dom";
import {Button, Stack, Container, Typography, TextField} from '@mui/material';
import toast from 'react-hot-toast';
import { DataGrid } from '@mui/x-data-grid';

const Relatorio = ({stub}) => {
  const navigate = useNavigate();

  const [dataIni, setDataIni] = useState('');
  const [dataFim, setDataFim] = useState('');
  const [horaIni, setHoraIni] = useState('');
  const [horaFim, setHoraFim] = useState('');

  const [formReady, setFormReady] = useState(false);

  const [relatorioAtual, setRelatorioAtual] = useState('');

  useEffect(() => {
    // console.log(formData);
    let ok = true;
    if (dataIni === '' || horaIni === '' || dataFim === '' || horaFim === '') {
      ok = false;
    }
    setFormReady(ok);
  }, [dataIni, dataFim, horaIni, horaFim]);

  function handleDataIniChange(e) {
    setDataIni(e.target.value);
  }

  function handleDataFimChange(e) {
    setDataFim(e.target.value);
  }

  function handleHoraIniChange(e) {
    setHoraIni(e.target.value);
  }

  function handleHoraFimChange(e) {
    setHoraFim(e.target.value);
  }

  const estoque_cols = [
    { field: 'id', headerName: 'Código', width: 70 },
    { field: 'quantidade', headerName: 'Quantidade', width: 130 }
  ];
  
  const [estoqueRows, setEstoqueRows] = useState([]);

  const movimentacoes_cols = [
    { field: 'id', headerName: 'Data e hora', width: 140 },
    { field: 'tipo', headerName: 'Tipo', width: 100 },
    { field: 'codigo', headerName: 'Código', width: 80 },
    { field: 'quantidade', headerName: 'Quantidade', width: 90 },
    { field: 'nome', headerName: 'Nome', width: 100 },
    { field: 'descricao', headerName: 'Descrição', width: 100 },
    { field: 'preco_unitario', headerName: 'Preço Unitário', width: 120 },
    { field: 'estoque_minimo', headerName: 'Estoque mínimo', width: 120 },
  ];
  
  const [movimentacoesRows, setMovimentacoesRows] = useState([]);

  const sem_saida_cols = [
    { field: 'id', headerName: 'Código', width: 70 },
  ];
  
  const [semSaidaRows, setSemSaidaRows] = useState([]);

  function get_lancamento_callback(tipoRelatorio) {
    const lancamento_callback = (error, estadoResposta) => {
      console.log(error);
      console.log(estadoResposta);
      if (error) {
        return;
      }
      toast('Relatório recebido');
      setRelatorioAtual(tipoRelatorio);
      if (tipoRelatorio === 'estoque') {
        let estoque_rows = [];
        for (let codigo in estadoResposta.estoque) {
          estoque_rows.push({id: codigo, quantidade: estadoResposta.estoque[codigo]});
        }
        setEstoqueRows(estoque_rows);
      } else if (tipoRelatorio === 'movimentacoes') {
        let movimentacoes_rows = [];
        for (let mov of estadoResposta.movimentacoes) {
          console.log(mov);
          movimentacoes_rows.push({
            id: mov.data_movimentacao,
            tipo: mov.tipo,
            codigo: mov.codigo,
            quantidade: mov.quantidade,
            nome: mov.nome,
            descricao: mov.descricao,
            preco_unitario: mov.preco_unitario,
            estoque_minimo: mov.estoque_minimo
          });
        }
        console.log(movimentacoes_rows);
        setMovimentacoesRows(movimentacoes_rows);
      } else if (tipoRelatorio === 'semsaida') {
        let semsaida_rows = [];
        for (let codigo in estadoResposta.codigos_sem_saida) {
          semsaida_rows.push({id: codigo});
        }
        setSemSaidaRows(semsaida_rows);
      }
    }
    return lancamento_callback;
  }

  const handleRelatorioEstoque = (e) => {
    stub.ObterRelatorioEstoque({}, get_lancamento_callback('estoque'));
  };

  const handleRelatorioMovimentacoes = (e) => {
    stub.ObterRelatorioFluxoMovimentacoes({
      inicio_periodo: dataIni + 'T' + horaIni,
      fim_periodo: dataFim + 'T' + horaFim,
    }, get_lancamento_callback('movimentacoes'));
  };

  const handleRelatorioSemSaida = (e) => {
    stub.ObterRelatorioSemSaida({
      inicio_periodo: dataIni + 'T' + horaIni,
      fim_periodo: dataFim + 'T' + horaFim,
    }, get_lancamento_callback('semsaida'));
  };
  
  const handleVoltar = (e) => {
    navigate('/');
  };
  
  const handleVoltarRelatorio = (e) => {
    setRelatorioAtual('');
  };

  return (
    <Container>
        {
          relatorioAtual === '' &&
          <Stack
            spacing={2}
            direction="column"
            justifyContent="center"
            alignItems="center"
            display="flex" 
            flexDirection="column"
          >
            <Typography variant="h4" gutterBottom>
              Geração de relatórios
            </Typography>
            <Stack
              spacing={2}
              direction="row"
              justifyContent="center"
              alignItems="center"
              display="flex" 
              flexDirection="row"
            >
              <Typography variant="h7" gutterBottom>
                Início período:
              </Typography>
              <TextField
              label="Data"
              value={dataIni}
              onChange={handleDataIniChange}
              size="small"
              autoComplete="off"
            />
              <TextField
              label="Horário"
              value={horaIni}
              onChange={handleHoraIniChange}
              size="small"
              autoComplete="off"
            />
            </Stack>
            <Stack
              spacing={2}
              direction="row"
              justifyContent="center"
              alignItems="center"
              display="flex" 
              flexDirection="row"
            >
              <Typography variant="h7" gutterBottom>
                Final período:
              </Typography>
              <TextField
              label="Data"
              value={dataFim}
              onChange={handleDataFimChange}
              size="small"
              autoComplete="off"
            />
              <TextField
              label="Horário"
              value={horaFim}
              onChange={handleHoraFimChange}
              size="small"
              autoComplete="off"
            />
            </Stack>
            <Button variant="contained" onClick={handleRelatorioEstoque}>Gerar relatório de estoque</Button>
            <Button variant="contained" onClick={handleRelatorioMovimentacoes} disabled={!formReady}>Gerar relatório de movimentações</Button>
            <Button variant="contained" onClick={handleRelatorioSemSaida} disabled={!formReady}>Gerar relatório sem saída</Button>
            <Button variant="contained" onClick={handleVoltar} color="secondary">Voltar</Button>
          </Stack>
        }
        {
          relatorioAtual === 'estoque' &&
          <Stack
            spacing={2}
            direction="column"
            justifyContent="center"
            alignItems="center"
            display="flex" 
            flexDirection="column"
          >
            <Typography variant="h4" gutterBottom>
              Relatório de Estoque
            </Typography>
            <DataGrid
              rows={estoqueRows}
              columns={estoque_cols}
              initialState={{
                pagination: {
                  paginationModel: { page: 0, pageSize: 5 },
                },
              }}
              pageSizeOptions={[5, 10]}
            />
            <Stack
              spacing={2}
              direction="row"
              justifyContent="center"
              alignItems="center"
              display="flex" 
              flexDirection="row"
            >
              <Button variant="contained" onClick={handleVoltarRelatorio} color="secondary">Voltar para relatório</Button>
              <Button variant="contained" onClick={handleVoltar} color="secondary">Voltar para Menu</Button>
            </Stack>
          </Stack>
        }
        {
          relatorioAtual === 'movimentacoes' &&
          <Stack
            spacing={2}
            direction="column"
            justifyContent="center"
            alignItems="center"
            display="flex" 
            flexDirection="column"
          >
            <Typography variant="h4" gutterBottom>
              Relatório de Movimentações
            </Typography>
            <DataGrid
              rows={movimentacoesRows}
              columns={movimentacoes_cols}
              initialState={{
                pagination: {
                  paginationModel: { page: 0, pageSize: 5 },
                },
              }}
              pageSizeOptions={[5, 10]}
            />
            <Stack
              spacing={2}
              direction="row"
              justifyContent="center"
              alignItems="center"
              display="flex" 
              flexDirection="row"
            >
              <Button variant="contained" onClick={handleVoltarRelatorio} color="secondary">Voltar para relatório</Button>
              <Button variant="contained" onClick={handleVoltar} color="secondary">Voltar para Menu</Button>
            </Stack>
          </Stack>
        }
        {
          relatorioAtual === 'semsaida' &&
          <Stack
            spacing={2}
            direction="column"
            justifyContent="center"
            alignItems="center"
            display="flex" 
            flexDirection="column"
          >
            <Typography variant="h4" gutterBottom>
              Relatório Sem Saída
            </Typography>
            <DataGrid
              rows={semSaidaRows}
              columns={sem_saida_cols}
              initialState={{
                pagination: {
                  paginationModel: { page: 0, pageSize: 5 },
                },
              }}
              pageSizeOptions={[5, 10]}
            />
            <Stack
              spacing={2}
              direction="row"
              justifyContent="center"
              alignItems="center"
              display="flex" 
              flexDirection="row"
            >
              <Button variant="contained" onClick={handleVoltarRelatorio} color="secondary">Voltar para relatório</Button>
              <Button variant="contained" onClick={handleVoltar} color="secondary">Voltar para Menu</Button>
            </Stack>
          </Stack>
        }
      </Container>
  );
};
export default Relatorio;