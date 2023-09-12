#!/usr/bin/env python
import pika, sys, os, argparse

# dicionários para identificar tópicos pelos números
topico = dict()
topico[1] = "peixes"
topico[2] = "assistencia.mecanica"
topico[3] = "assistencia.iscas"
topico[4] = "assistencia.cheio"
topico[5] = "assistencia.outra"

descr = dict()
descr[1] = "tópico peixes"
descr[2] = "tópico assistência mecânica"
descr[3] = "tópico assistência com iscas"
descr[4] = "tópico assistência com compartimento cheio"
descr[5] = "tópico outra assistência"

# função que só imprime o que foi mandado caso a opção debug esteja ativada
def debug_print(s):
    if args.debug:
        print(s)

# usa módulo argparse do python para descrever argumentos do programa
parser = argparse.ArgumentParser(description='Subscriber de uma aplicação de competição de pesca')
parser.add_argument('--debug', action='store_true', help='Escreve informações de debug')

args = parser.parse_args()

def main():
    # conecta no broker do rabbitmq
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # declara a exchange usada, do tipo tópico
    channel.exchange_declare(exchange='ex', exchange_type='topic')

    # cria uma queue exclusiva para esse subscriber e pega o nome dela
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    count = 0
    # pergunta para cada tópico se deseja se inscrever
    for i in range(1, 6):
        sub = input(f"Deseja se inscrever no {descr[i]}? (y/N)\n")
        if sub == "y":
            # cria bind entre a nossa queue e o tópico a se inscrever
            channel.queue_bind(queue=queue_name, exchange='ex', routing_key=topico[i])
            count += 1

    # fecha programa se não se inscreveu em nada
    if count == 0:
        return


    # função que vai ser chamada quando receber mensagem
    def callback(ch, method, properties, body):
        debug_print(f' [x] Received {body}')
        print(body.decode('utf-8'))

    # associa a função acima com mensagens recebidas na nossa queue;
    # usa opção para mandar ack automaticamente
    # (caso contrário precisaria usar a função de basic_ack no callback)
    channel.basic_consume(queue=queue_name, auto_ack=True, on_message_callback=callback)
    print('Pronto para receber mensagens. Para sair pressione CTRL+C.')

    # bloqueia e espera por mensagens
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nSaindo')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)