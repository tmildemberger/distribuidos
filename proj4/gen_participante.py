# bibliotecas do python
import argparse
import json

from pathlib import Path

# biblioteca cryptography para assinatura e verificação com chaves rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, utils, padding

# usa módulo argparse do python para descrever argumentos do programa
parser = argparse.ArgumentParser(description='Gerador de participantes')
parser.add_argument('nome', help='Nome do participante')
parser.add_argument('porta', help='Porta do participante')
# parser.add_argument('--debug', action='store_true', help='Escreve informações de debug')

args = parser.parse_args()

part = Path('.') / args.nome
if part.exists() and part.is_dir():
    import sys
    print(f"{args.nome} parece já ser um participante existente")
    sys.exit(f"{args.nome} parece já ser um participante existente")

part_obj = dict()
part_obj['nome'] = args.nome
part_obj['porta'] = args.porta

part.mkdir()

(part / 'desc.json').write_text(json.dumps(part_obj, indent=4))

private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

serialized_public_key = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
).decode('utf-8')

serialized_private_key = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
).decode('utf-8')

(part / 'key.pub').write_text(serialized_public_key)
(part / 'key').write_text(serialized_private_key)

(part / 'servers.json').write_text(json.dumps([], indent=4))
(part / 'shards.json').write_text(json.dumps([], indent=4))