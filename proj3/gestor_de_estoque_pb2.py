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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x17gestor_de_estoque.proto\"\x0f\n\rMensagemVazia\" \n\x0e\x45stadoResposta\x12\x0e\n\x06\x65stado\x18\x01 \x01(\t\"\x1d\n\rDadosCadastro\x12\x0c\n\x04nome\x18\x01 \x01(\t\"\x15\n\x06SseUrl\x12\x0b\n\x03url\x18\x01 \x01(\t\"\x83\x01\n\x0c\x44\x61\x64osEntrada\x12\x0e\n\x06\x63odigo\x18\x01 \x01(\t\x12\x12\n\nquantidade\x18\x02 \x01(\x05\x12\x0c\n\x04nome\x18\x03 \x01(\t\x12\x11\n\tdescricao\x18\x04 \x01(\t\x12\x16\n\x0epreco_unitario\x18\x05 \x01(\x05\x12\x16\n\x0e\x65stoque_minimo\x18\x06 \x01(\x05\"0\n\nDadosSaida\x12\x0e\n\x06\x63odigo\x18\x01 \x01(\t\x12\x12\n\nquantidade\x18\x02 \x01(\x05\"6\n\x07Periodo\x12\x16\n\x0einicio_periodo\x18\x01 \x01(\t\x12\x13\n\x0b\x66im_periodo\x18\x02 \x01(\t\"s\n\x10RelatorioEstoque\x12/\n\x07\x65stoque\x18\x01 \x03(\x0b\x32\x1e.RelatorioEstoque.EstoqueEntry\x1a.\n\x0c\x45stoqueEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\"\xdf\x02\n\x1bRelatorioFluxoMovimentacoes\x12@\n\rmovimentacoes\x18\x01 \x03(\x0b\x32).RelatorioFluxoMovimentacoes.Movimentacao\x1a\xfd\x01\n\x0cMovimentacao\x12\x0c\n\x04tipo\x18\x01 \x01(\t\x12\x0e\n\x06\x63odigo\x18\x02 \x01(\t\x12\x12\n\nquantidade\x18\x03 \x01(\x05\x12\x19\n\x11\x64\x61ta_movimentacao\x18\x04 \x01(\t\x12\x11\n\x04nome\x18\x05 \x01(\tH\x00\x88\x01\x01\x12\x16\n\tdescricao\x18\x06 \x01(\tH\x01\x88\x01\x01\x12\x1b\n\x0epreco_unitario\x18\x07 \x01(\x05H\x02\x88\x01\x01\x12\x1b\n\x0e\x65stoque_minimo\x18\x08 \x01(\x05H\x03\x88\x01\x01\x42\x07\n\x05_nomeB\x0c\n\n_descricaoB\x11\n\x0f_preco_unitarioB\x11\n\x0f_estoque_minimo\".\n\x11RelatorioSemSaida\x12\x19\n\x11\x63odigos_sem_saida\x18\x01 \x03(\t2\xd5\x02\n\x0fGestorDeEstoque\x12$\n\tCadastrar\x12\x0e.DadosCadastro\x1a\x07.SseUrl\x12:\n\x15ObterRelatorioEstoque\x12\x0e.MensagemVazia\x1a\x11.RelatorioEstoque\x12J\n ObterRelatorioFluxoMovimentacoes\x12\x08.Periodo\x1a\x1c.RelatorioFluxoMovimentacoes\x12\x36\n\x16ObterRelatorioSemSaida\x12\x08.Periodo\x1a\x12.RelatorioSemSaida\x12/\n\rLancarEntrada\x12\r.DadosEntrada\x1a\x0f.EstadoResposta\x12+\n\x0bLancarSaida\x12\x0b.DadosSaida\x1a\x0f.EstadoRespostab\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'gestor_de_estoque_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _RELATORIOESTOQUE_ESTOQUEENTRY._options = None
  _RELATORIOESTOQUE_ESTOQUEENTRY._serialized_options = b'8\001'
  _globals['_MENSAGEMVAZIA']._serialized_start=27
  _globals['_MENSAGEMVAZIA']._serialized_end=42
  _globals['_ESTADORESPOSTA']._serialized_start=44
  _globals['_ESTADORESPOSTA']._serialized_end=76
  _globals['_DADOSCADASTRO']._serialized_start=78
  _globals['_DADOSCADASTRO']._serialized_end=107
  _globals['_SSEURL']._serialized_start=109
  _globals['_SSEURL']._serialized_end=130
  _globals['_DADOSENTRADA']._serialized_start=133
  _globals['_DADOSENTRADA']._serialized_end=264
  _globals['_DADOSSAIDA']._serialized_start=266
  _globals['_DADOSSAIDA']._serialized_end=314
  _globals['_PERIODO']._serialized_start=316
  _globals['_PERIODO']._serialized_end=370
  _globals['_RELATORIOESTOQUE']._serialized_start=372
  _globals['_RELATORIOESTOQUE']._serialized_end=487
  _globals['_RELATORIOESTOQUE_ESTOQUEENTRY']._serialized_start=441
  _globals['_RELATORIOESTOQUE_ESTOQUEENTRY']._serialized_end=487
  _globals['_RELATORIOFLUXOMOVIMENTACOES']._serialized_start=490
  _globals['_RELATORIOFLUXOMOVIMENTACOES']._serialized_end=841
  _globals['_RELATORIOFLUXOMOVIMENTACOES_MOVIMENTACAO']._serialized_start=588
  _globals['_RELATORIOFLUXOMOVIMENTACOES_MOVIMENTACAO']._serialized_end=841
  _globals['_RELATORIOSEMSAIDA']._serialized_start=843
  _globals['_RELATORIOSEMSAIDA']._serialized_end=889
  _globals['_GESTORDEESTOQUE']._serialized_start=892
  _globals['_GESTORDEESTOQUE']._serialized_end=1233
# @@protoc_insertion_point(module_scope)