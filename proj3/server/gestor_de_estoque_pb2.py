# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: gestor_de_estoque.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x17gestor_de_estoque.proto\x12\x11gestor_de_estoque\"\x0f\n\rMensagemVazia\" \n\x0e\x45stadoResposta\x12\x0e\n\x06\x65stado\x18\x01 \x01(\t\"\x1d\n\rDadosCadastro\x12\x0c\n\x04nome\x18\x01 \x01(\t\"\x15\n\x06SseUrl\x12\x0b\n\x03url\x18\x01 \x01(\t\"\x83\x01\n\x0c\x44\x61\x64osEntrada\x12\x0e\n\x06\x63odigo\x18\x01 \x01(\t\x12\x12\n\nquantidade\x18\x02 \x01(\x05\x12\x0c\n\x04nome\x18\x03 \x01(\t\x12\x11\n\tdescricao\x18\x04 \x01(\t\x12\x16\n\x0epreco_unitario\x18\x05 \x01(\x05\x12\x16\n\x0e\x65stoque_minimo\x18\x06 \x01(\x05\"0\n\nDadosSaida\x12\x0e\n\x06\x63odigo\x18\x01 \x01(\t\x12\x12\n\nquantidade\x18\x02 \x01(\x05\"6\n\x07Periodo\x12\x16\n\x0einicio_periodo\x18\x01 \x01(\t\x12\x13\n\x0b\x66im_periodo\x18\x02 \x01(\t\"\x85\x01\n\x10RelatorioEstoque\x12\x41\n\x07\x65stoque\x18\x01 \x03(\x0b\x32\x30.gestor_de_estoque.RelatorioEstoque.EstoqueEntry\x1a.\n\x0c\x45stoqueEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\"\xf1\x02\n\x1bRelatorioFluxoMovimentacoes\x12R\n\rmovimentacoes\x18\x01 \x03(\x0b\x32;.gestor_de_estoque.RelatorioFluxoMovimentacoes.Movimentacao\x1a\xfd\x01\n\x0cMovimentacao\x12\x0c\n\x04tipo\x18\x01 \x01(\t\x12\x0e\n\x06\x63odigo\x18\x02 \x01(\t\x12\x12\n\nquantidade\x18\x03 \x01(\x05\x12\x19\n\x11\x64\x61ta_movimentacao\x18\x04 \x01(\t\x12\x11\n\x04nome\x18\x05 \x01(\tH\x00\x88\x01\x01\x12\x16\n\tdescricao\x18\x06 \x01(\tH\x01\x88\x01\x01\x12\x1b\n\x0epreco_unitario\x18\x07 \x01(\x05H\x02\x88\x01\x01\x12\x1b\n\x0e\x65stoque_minimo\x18\x08 \x01(\x05H\x03\x88\x01\x01\x42\x07\n\x05_nomeB\x0c\n\n_descricaoB\x11\n\x0f_preco_unitarioB\x11\n\x0f_estoque_minimo\".\n\x11RelatorioSemSaida\x12\x19\n\x11\x63odigos_sem_saida\x18\x01 \x03(\t2\xad\x04\n\x0fGestorDeEstoque\x12H\n\tCadastrar\x12 .gestor_de_estoque.DadosCadastro\x1a\x19.gestor_de_estoque.SseUrl\x12^\n\x15ObterRelatorioEstoque\x12 .gestor_de_estoque.MensagemVazia\x1a#.gestor_de_estoque.RelatorioEstoque\x12n\n ObterRelatorioFluxoMovimentacoes\x12\x1a.gestor_de_estoque.Periodo\x1a..gestor_de_estoque.RelatorioFluxoMovimentacoes\x12Z\n\x16ObterRelatorioSemSaida\x12\x1a.gestor_de_estoque.Periodo\x1a$.gestor_de_estoque.RelatorioSemSaida\x12S\n\rLancarEntrada\x12\x1f.gestor_de_estoque.DadosEntrada\x1a!.gestor_de_estoque.EstadoResposta\x12O\n\x0bLancarSaida\x12\x1d.gestor_de_estoque.DadosSaida\x1a!.gestor_de_estoque.EstadoRespostab\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'gestor_de_estoque_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _RELATORIOESTOQUE_ESTOQUEENTRY._options = None
  _RELATORIOESTOQUE_ESTOQUEENTRY._serialized_options = b'8\001'
  _globals['_MENSAGEMVAZIA']._serialized_start=46
  _globals['_MENSAGEMVAZIA']._serialized_end=61
  _globals['_ESTADORESPOSTA']._serialized_start=63
  _globals['_ESTADORESPOSTA']._serialized_end=95
  _globals['_DADOSCADASTRO']._serialized_start=97
  _globals['_DADOSCADASTRO']._serialized_end=126
  _globals['_SSEURL']._serialized_start=128
  _globals['_SSEURL']._serialized_end=149
  _globals['_DADOSENTRADA']._serialized_start=152
  _globals['_DADOSENTRADA']._serialized_end=283
  _globals['_DADOSSAIDA']._serialized_start=285
  _globals['_DADOSSAIDA']._serialized_end=333
  _globals['_PERIODO']._serialized_start=335
  _globals['_PERIODO']._serialized_end=389
  _globals['_RELATORIOESTOQUE']._serialized_start=392
  _globals['_RELATORIOESTOQUE']._serialized_end=525
  _globals['_RELATORIOESTOQUE_ESTOQUEENTRY']._serialized_start=479
  _globals['_RELATORIOESTOQUE_ESTOQUEENTRY']._serialized_end=525
  _globals['_RELATORIOFLUXOMOVIMENTACOES']._serialized_start=528
  _globals['_RELATORIOFLUXOMOVIMENTACOES']._serialized_end=897
  _globals['_RELATORIOFLUXOMOVIMENTACOES_MOVIMENTACAO']._serialized_start=644
  _globals['_RELATORIOFLUXOMOVIMENTACOES_MOVIMENTACAO']._serialized_end=897
  _globals['_RELATORIOSEMSAIDA']._serialized_start=899
  _globals['_RELATORIOSEMSAIDA']._serialized_end=945
  _globals['_GESTORDEESTOQUE']._serialized_start=948
  _globals['_GESTORDEESTOQUE']._serialized_end=1505
# @@protoc_insertion_point(module_scope)
