# bibliotecas do python
import argparse
import json
import threading
import time
import pprint

import Pyro5.api

# biblioteca cryptography para assinatura e verificação com chaves rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, utils, padding

# biblioteca prompt_toolkit para interface com o usuário
from prompt_toolkit import prompt
from prompt_toolkit.patch_stdout import patch_stdout

# configura uso do serializer 'marshal'
Pyro5.config.SERIALIZER = 'marshal'

# usa módulo argparse do python para descrever argumentos do programa
parser = argparse.ArgumentParser(description='Cliente do gerenciador de estoque')
parser.add_argument('nome', nargs='?', default='???', help='Número ou nome do gestor (opcional)')
parser.add_argument('--debug', action='store_true', help='Escreve informações de debug')

args = parser.parse_args()

# função que só imprime o que foi mandado caso a opção debug esteja ativada
def debug_print(s):
    if args.debug:
        print(s)


class Client(object):
    def __init__(self, nome, daemon, proxy_servidor):
        self.daemon = daemon
        self.proxy_servidor = proxy_servidor
        self.nome = nome
        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.public_key = self.private_key.public_key()
        self.serialized_public_key = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')
        self.prompts = dict()
        self.prompts["comando"] = ">> "
        self.prompts["entrada"] = "Entrada>> "
        self.prompts["saida"] = "Saída>> "
        self.prompts["relatorio"] = "Relatório>> "
        self.prompts["sair"] = ""

        self.states_entry = dict()
        self.states_entry["comando"] = self.default_entry
        self.states_entry["entrada"] = self.entrada_entry
        self.states_entry["saida"] = self.saida_entry
        self.states_entry["relatorio"] = self.relatorio_entry

        self.states = dict()
        self.states["comando"] = self.comando
        self.states["entrada"] = self.entrada
        self.states["saida"] = self.saida
        self.states["relatorio"] = self.relatorio
        
    def help():
        print("Comandos disponíveis:")
        print("  >> entrada (ou somente 'e')")
        print("  -- coloca a entrada de um determinado produto no estoque;")
        print("  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("  >> saída (ou somente 's')")
        print("  -- realiza a saída de algum produto do estoque")
        print("  ++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("  >> relatório (ou somente 'r')")
        print("  -- recebe o relatório de produtos não vendidos")
        print("  ++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("  >> help (ou somente 'h')")
        print("  -- mostra essa mensagem de comandos disponíveis")
        print("  +++++++++++++++++++++++++++++++++++++++++++++++")
        print("  >> quit")
        print("  -- fecha a conexão e sai do programa")
        print("  ++++++++++++++++++++++++++++++++++++")

    def default_entry(self):
        self.prompt = self.prompts[self.state]
        pass
    
    def comando(self, msg):
        # processa comando
        tokens = msg.split()
        if tokens[0] == 'entrada' or tokens[0] == 'e':
            return "entrada"
        elif tokens[0] == 'saida' or tokens[0] == 's':
            return "saida"
        elif tokens[0] == 'relatorio' or tokens[0] == 'r':
            return "relatorio"
        elif tokens[0] == 'help' or tokens[0] == 'h':
            self.help()
            return "comando"
        elif tokens[0] == 'quit' or tokens[0] == 'q':
            return "sair"
        else:
            return "comando"

    def entrada_entry(self):
        self.entrada_fields = ["Código", "Nome", "Descrição", "Quantidade", "Preço Unitário", "Estoque Mínimo"]
        self.entrada_state = 0
        self.entrada_data = dict()
        self.prompt = self.prompts["entrada"] + self.entrada_fields[self.entrada_state] + ">> "

    def entrada(self, msg):
        self.entrada_data[self.entrada_fields[self.entrada_state]] = msg
        self.entrada_state += 1
        if self.entrada_state >= len(self.entrada_fields):
            # irá enviar mensagem
            message = json.dumps(self.entrada_data)
            message_bytes = bytes(message, 'utf-8')
            signature = self.private_key.sign(
                message_bytes,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            debug_print(f"enviando mensagem")
            debug_print(self.entrada_data)
            self.proxy_servidor.lancamento_entrada(self.nome, message, signature)
            return "comando"
        
        self.prompt = self.prompts["entrada"] + self.entrada_fields[self.entrada_state] + ">> "
        return "entrada"
    
    def saida_entry(self):
        self.saida_fields = ["Código", "Quantidade"]
        self.saida_state = 0
        self.saida_data = dict()
        self.prompt = self.prompts["saida"] + self.saida_fields[self.saida_state] + ">> "

    def saida(self, msg):
        self.saida_data[self.saida_fields[self.saida_state]] = msg
        self.saida_state += 1
        if self.saida_state >= len(self.saida_fields):
            # irá enviar mensagem
            message = json.dumps(self.saida_data)
            message_bytes = bytes(message, 'utf-8')
            signature = self.private_key.sign(
                message_bytes,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            debug_print(f"enviando mensagem")
            debug_print(self.saida_data)
            self.proxy_servidor.lancamento_saida(self.nome, message, signature)
            return "comando"
        
        self.prompt = self.prompts["saida"] + self.saida_fields[self.saida_state] + ">> "
        return "saida"
    
    def relatorio_entry(self):
        self.relatorio_prompts = ["Tipo de Relatório ('Estoque', 'Histórico', 'Sem saída')", "Data inicial (formato YYYY-MM-DD)", "Hora inicial (formato hh:mm:ss)", "Data final", "Hora final"]
        self.relatorio_fields = ['tipo', 'd_st', 'h_st', 'd_ed', 'h_ed']
        self.relatorio_state = 0
        self.relatorio_data = dict()
        self.prompt = self.prompts["relatorio"] + self.relatorio_prompts[self.relatorio_state] + ">> "

    def relatorio(self, msg):
        self.relatorio_data[self.relatorio_fields[self.relatorio_state]] = msg
        self.relatorio_state += 1
        tipo = self.relatorio_data["tipo"]
        tipo = tipo.lower()
        if tipo == 'estoque' or tipo == 'e':
            resp = self.proxy_servidor.relatorio_estoque()
            debug_print(f"recebendo relatório de estoque")
            debug_print(resp)
            for (codigo, quantidade) in resp.items():
                print(f"Produto {codigo} tem {quantidade} de estoque")
            return 'comando'
        elif self.relatorio_state >= len(self.relatorio_prompts):
            if tipo == 'histórico' or tipo == 'historico' or tipo == 'h':
                resp = self.proxy_servidor.relatorio_fluxo_movimentacoes(
                    self.relatorio_data['d_st'] + "T" + self.relatorio_data['h_st'],
                    self.relatorio_data['d_ed'] + "T" + self.relatorio_data['h_ed']
                )
                debug_print(f"recebendo relatório de historico")
                debug_print(resp)
                print("Fluxo de Movimentações no período:")
                pprint.pprint(resp)
            elif tipo == 'sem_saida' or tipo == 'sem saida' or tipo == 'sem saída' or tipo == 's':
                resp = self.proxy_servidor.relatorio_sem_saida(
                    self.relatorio_data['d_st'] + "T" + self.relatorio_data['h_st'],
                    self.relatorio_data['d_ed'] + "T" + self.relatorio_data['h_ed']
                )
                debug_print(f"recebendo relatório de sem_saida")
                debug_print(resp)
                print("Produtos sem saída no período:")
                pprint.pprint(resp)
            
            return "comando"
        
        self.prompt = self.prompts["relatorio"] + self.relatorio_prompts[self.relatorio_state] + ">> "
        return "relatorio"
    
    @Pyro5.api.expose
    @Pyro5.api.callback
    def notificacao(self, tipo, mensagem):
        print(f"\rNotificação {tipo}: {mensagem}")

    def run(self):
        self.proxy_servidor.cadastro(self.nome, self.serialized_public_key, self.daemon.uriFor(self))
        self.state = ""
        next_state = "comando"
        while next_state != "sair":
            if next_state != self.state:
                self.state = next_state
                self.states_entry[self.state]()

            # recebe comando/mensagem
            try:
                with patch_stdout():
                    msg = prompt(self.prompt)
            except (EOFError, KeyboardInterrupt):
                print()
                break

            # processa o que foi recebido
            next_state = self.states[self.state](msg)

# proxy para o servidor (já cadastrado no servidor de nomes)
server = Pyro5.api.Proxy("PYRONAME:gerenciador_de_estoque.servidor")

daemon = Pyro5.server.Daemon()

# cria e registra o objeto do cliente no daemon
debug_print(f"Criando objeto para o 'cliente{args.nome}'")
client = Client('cliente' + args.nome, daemon, server)
client_uri = daemon.register(client)

# inicia thread em background para o loop do daemon do Pyro
th = threading.Thread(target=daemon.requestLoop)
th.daemon = True
th.start()

# inicia função principal, que recebe entrada do usuário e se comunica com servidor
client.run()