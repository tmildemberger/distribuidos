# bibliotecas do python
import json

from pathlib import Path

from fastapi import FastAPI, HTTPException

app = FastAPI()

# biblioteca cryptography para assinatura e verificação com chaves rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, utils, padding

if not Path("./desc.json").exists():
    import sys
    print("Arquivo 'desc.json' não encontrado")
    sys.exit("Arquivo 'desc.json' não encontrado")

part_obj = json.loads(Path("./desc.json").read_text())
nome = part_obj['nome']

if not Path("./key").exists() or not Path("./key.pub").exists() or not Path("./log").exists():
    import sys
    print("Participante não foi inicializado corretamente")
    sys.exit("Participante não foi inicializado corretamente")

public_key = serialization.load_pem_public_key(bytes(Path("./key.pub").read_text(), 'utf-8'))
private_key = serialization.load_pem_private_key(bytes(Path("./key").read_text(), 'utf-8'), password=None)


#######
@app.post('/prepare')
def prepare():
    global vote
    #Guardar todas as informações necessárias antes de dar o voto
    vote = 'YES'
    return vote


@app.get('/commit')
def commit():
    #Commitar caso o coordenador tenha a decision de commit 
    global vote
    if vote == 'YES'
        return {'decision':'COMMIT'}
    else
        return {'decision':'ABORT'}

