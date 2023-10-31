from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MensagemVazia(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class EstadoResposta(_message.Message):
    __slots__ = ["estado"]
    ESTADO_FIELD_NUMBER: _ClassVar[int]
    estado: str
    def __init__(self, estado: _Optional[str] = ...) -> None: ...

class DadosCadastro(_message.Message):
    __slots__ = ["nome"]
    NOME_FIELD_NUMBER: _ClassVar[int]
    nome: str
    def __init__(self, nome: _Optional[str] = ...) -> None: ...

class SseUrl(_message.Message):
    __slots__ = ["url"]
    URL_FIELD_NUMBER: _ClassVar[int]
    url: str
    def __init__(self, url: _Optional[str] = ...) -> None: ...

class DadosEntrada(_message.Message):
    __slots__ = ["codigo", "quantidade", "nome", "descricao", "preco_unitario", "estoque_minimo"]
    CODIGO_FIELD_NUMBER: _ClassVar[int]
    QUANTIDADE_FIELD_NUMBER: _ClassVar[int]
    NOME_FIELD_NUMBER: _ClassVar[int]
    DESCRICAO_FIELD_NUMBER: _ClassVar[int]
    PRECO_UNITARIO_FIELD_NUMBER: _ClassVar[int]
    ESTOQUE_MINIMO_FIELD_NUMBER: _ClassVar[int]
    codigo: str
    quantidade: int
    nome: str
    descricao: str
    preco_unitario: int
    estoque_minimo: int
    def __init__(self, codigo: _Optional[str] = ..., quantidade: _Optional[int] = ..., nome: _Optional[str] = ..., descricao: _Optional[str] = ..., preco_unitario: _Optional[int] = ..., estoque_minimo: _Optional[int] = ...) -> None: ...

class DadosSaida(_message.Message):
    __slots__ = ["codigo", "quantidade"]
    CODIGO_FIELD_NUMBER: _ClassVar[int]
    QUANTIDADE_FIELD_NUMBER: _ClassVar[int]
    codigo: str
    quantidade: int
    def __init__(self, codigo: _Optional[str] = ..., quantidade: _Optional[int] = ...) -> None: ...

class Periodo(_message.Message):
    __slots__ = ["inicio_periodo", "fim_periodo"]
    INICIO_PERIODO_FIELD_NUMBER: _ClassVar[int]
    FIM_PERIODO_FIELD_NUMBER: _ClassVar[int]
    inicio_periodo: str
    fim_periodo: str
    def __init__(self, inicio_periodo: _Optional[str] = ..., fim_periodo: _Optional[str] = ...) -> None: ...

class RelatorioEstoque(_message.Message):
    __slots__ = ["estoque"]
    class EstoqueEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    ESTOQUE_FIELD_NUMBER: _ClassVar[int]
    estoque: _containers.ScalarMap[str, int]
    def __init__(self, estoque: _Optional[_Mapping[str, int]] = ...) -> None: ...

class RelatorioFluxoMovimentacoes(_message.Message):
    __slots__ = ["movimentacoes"]
    class Movimentacao(_message.Message):
        __slots__ = ["tipo", "codigo", "quantidade", "data_movimentacao", "nome", "descricao", "preco_unitario", "estoque_minimo"]
        TIPO_FIELD_NUMBER: _ClassVar[int]
        CODIGO_FIELD_NUMBER: _ClassVar[int]
        QUANTIDADE_FIELD_NUMBER: _ClassVar[int]
        DATA_MOVIMENTACAO_FIELD_NUMBER: _ClassVar[int]
        NOME_FIELD_NUMBER: _ClassVar[int]
        DESCRICAO_FIELD_NUMBER: _ClassVar[int]
        PRECO_UNITARIO_FIELD_NUMBER: _ClassVar[int]
        ESTOQUE_MINIMO_FIELD_NUMBER: _ClassVar[int]
        tipo: str
        codigo: str
        quantidade: int
        data_movimentacao: str
        nome: str
        descricao: str
        preco_unitario: int
        estoque_minimo: int
        def __init__(self, tipo: _Optional[str] = ..., codigo: _Optional[str] = ..., quantidade: _Optional[int] = ..., data_movimentacao: _Optional[str] = ..., nome: _Optional[str] = ..., descricao: _Optional[str] = ..., preco_unitario: _Optional[int] = ..., estoque_minimo: _Optional[int] = ...) -> None: ...
    MOVIMENTACOES_FIELD_NUMBER: _ClassVar[int]
    movimentacoes: _containers.RepeatedCompositeFieldContainer[RelatorioFluxoMovimentacoes.Movimentacao]
    def __init__(self, movimentacoes: _Optional[_Iterable[_Union[RelatorioFluxoMovimentacoes.Movimentacao, _Mapping]]] = ...) -> None: ...

class RelatorioSemSaida(_message.Message):
    __slots__ = ["codigos_sem_saida"]
    CODIGOS_SEM_SAIDA_FIELD_NUMBER: _ClassVar[int]
    codigos_sem_saida: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, codigos_sem_saida: _Optional[_Iterable[str]] = ...) -> None: ...
