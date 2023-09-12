#!/usr/bin/env python
import pika, sys, argparse

# dicionários para identificar tópicos pelos números
topico = dict()
topico["1"] = "peixes"
topico["2"] = "assistencia.mecanica"
topico["3"] = "assistencia.iscas"
topico["4"] = "assistencia.cheio"
topico["5"] = "assistencia.outra"

prompt = dict()
prompt["0"] = ">> "
prompt["1"] = "Tópico peixes>> "
prompt["2"] = "Tópico assistência mecânica>> "
prompt["3"] = "Tópico assistência com iscas>> "
prompt["4"] = "Tópico assistência com compartimento cheio>> "
prompt["5"] = "Tópico outra assistência>> "

descr = dict()
descr[1] = "Tópico peixes"
descr[2] = "Tópico assistência mecânica"
descr[3] = "Tópico assistência com iscas"
descr[4] = "Tópico assistência com compartimento cheio"
descr[5] = "Tópico outra assistência"

# função que só imprime o que foi mandado caso a opção debug esteja ativada
def debug_print(s):
    if args.debug:
        print(s)

# imprime ajuda para interagir com o programa
def help():
    print("Comandos disponíveis:")
    print("  >> t [tópico]")
    print("  -- onde tópico é um número entre 1 e 5;")
    print("  == quando dentro de um tópico, apertar 'Enter' envia o que está")
    print("  == escrito para esse tópico, ou sai do tópico, se estiver vazio.")
    print("  == Para sair do envio de tópico, basta pressionar a tecla 'Enter'")
    print("  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("  >> topics (ou somente 'ts')")
    print("  -- mostra a equivalência entre número de 1 a 5 e tópicos")
    print("  ++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("  >> help (ou somente 'h')")
    print("  -- mostra essa mensagem de comandos disponíveis")
    print("  +++++++++++++++++++++++++++++++++++++++++++++++")
    print("  >> exit (ou somente 'e')")
    print("  -- fecha a conexão e sai do programa")
    print("  ++++++++++++++++++++++++++++++++++++")

# imprime relação entre número e tópico
def topics():
    print('++++')
    for i in range(1, 6):
        print(f"  {i} <-> {descr[i]}")
    print('++++')

# usa módulo argparse do python para descrever argumentos do programa
parser = argparse.ArgumentParser(description='Publisher de uma aplicação de competição de pesca')
parser.add_argument('nome', nargs='?', default='', help='Número ou nome do publisher (opcional)')
parser.add_argument('--debug', action='store_true', help='Escreve informações de debug')
parser.add_argument('--short', action='store_true', help='Envia mensagem curta (sem identificação do publisher)')

args = parser.parse_args()

# tenta obter nome para identificar o publisher caso não tenha recebido ainda
nome = args.nome
if nome == '':
    nome = input("Insira o número ou nome do publisher:\n")

if nome == '':
    nome = '???'

# imprime ajuda inicial
help()

# começa fora de qualquer tópico
state = '0'

# conecta no broker do rabbitmq
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# declara a exchange usada, do tipo tópico
channel.exchange_declare(exchange='ex', exchange_type='topic')

while True:
    # indica tópico atual
    print(prompt[state], end='')

    # recebe comando/mensagem
    try:
        msg = input()
    except EOFError:
        print()
        break

    # processa o que foi recebido
    if len(msg) == 0:
        state = '0'
    elif state != '0':
        # irá enviar mensagem
        body = msg if args.short else f"Pescador '{nome}' diz: {msg}"
        channel.basic_publish(exchange='ex', routing_key=topico[state], body=body)
        
        debug_print(f" [x] Sent {msg}, no tópico {topico[state]}")
    else:
        # processa comando
        tokens = msg.split()
        if tokens[0] == 't':
            if len(tokens) > 1 and tokens[1] in topico.keys() and tokens[1] != '0':
                state = tokens[1]
        elif tokens[0] == 'topics' or tokens[0] == 'ts':
            topics()
        elif tokens[0] == 'help' or tokens[0] == 'h':
            help()
        elif tokens[0] == 'exit' or tokens[0] == 'e':
            break

# fecha a conexão após terminar
connection.close()