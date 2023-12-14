from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel, PositiveInt, Field, Base64Bytes
from uuid import uuid4
from pathlib import Path

import json
import requests
import uvicorn
import base64

# biblioteca cryptography para assinatura e verificação com chaves rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, utils, padding

app = FastAPI()

class Shard(BaseModel):
    shard_id: str
    where: str
    name: str
    shard_type: str
    server_name: str
    shard_generator: str
    shard_index: PositiveInt

class Transaction(BaseModel):
    transaction_id: str
    status: str
    server_name: str
    description: List[Shard]


class OnlineParticipantMsg(BaseModel):
    name: str
    message: str
    signature: str
    key: str

# if not Path('./coordinator.json').exists():
#     import sys
#     print("Coordinator not initialized")
#     sys.exit("Coordinator not initialized")

if not Path('./serialized_keys.json').exists():
    Path('./serialized_keys.json').write_text(json.dumps({}))

transactions = dict()
serialized_keys = json.loads(Path('./serialized_keys.json').read_text())
keys = {k: serialization.load_pem_public_key(bytes(v, 'utf-8')) for k,v in serialized_keys.items()}
online_participants = dict()
active_transaction = False

@app.get("/transactions/{transaction_id}")
async def get_transactions(transaction_id: str):
    if transaction_id not in transactions.keys():
        print("Requested invalid transaction id")
        raise HTTPException(status_code=404, detail="Requested invalid transaction id")
    
    return transactions[transaction_id]

@app.get("/transactions")
async def get_transactions():
    return transactions

@app.post("/transactions")
async def post_transaction(transaction: Transaction):
    print(transaction)
    global active_transaction
    if active_transaction:
        print("One transaction is already active")
        raise HTTPException(status_code=409, detail="One transaction is already active")
    active_transaction = True
    transaction.status = 'Open'
    transactions[transaction.transaction_id] = transaction
    global decision
    decision = None

    try:
        # Fase 1: Envia a mensagem de voto para os participantes
        for participant_name, participant_uri in online_participants.items():
            response = requests.post(f'{participant_uri}/prepare', json=json.loads(transaction.model_dump_json()))
            if response.json().get('vote') != 'YES':
                raise Exception("Transaction aborted by participant")

        transaction.status = 'Prepared'

        # Fase 2: Confirmação ou anulação com base nos votos recebidos
        for participant_name, participant_uri in online_participants.items():
            response = requests.post(f'{participant_uri}/commit', json=json.loads(transaction.model_dump_json()))
            if response.json().get('decision') != 'COMMIT':
                raise Exception("Transaction aborted during commit phase")
        
        transaction.status = 'Committed'
        active_transaction = False
        decision = 'COMMIT'
        return {'status': 'Transaction committed'}

    except Exception as e:
        transaction.status = 'Aborted'

        decision = 'ABORT'
        active_transaction = False
        raise HTTPException(status_code=400, detail=f'Transaction aborted - {str(e)}')

@app.get("/online")
async def get_online():
    return online_participants

@app.post("/online")
async def post_online(online_message: OnlineParticipantMsg):
    uri = online_message.message
    sig = base64.decodebytes(bytes(online_message.signature, 'ascii'))
    if online_message.name not in serialized_keys.keys():
        # resp = requests.get(uri + '/public_key')
        # if resp.status_code not in [200, 201]:
        #     print(f"No public key ({resp.status_code})")
        #     raise HTTPException(status_code=401, detail="No public key")
        # public_key = serialization.load_pem_public_key(bytes(resp.json()['key'], 'utf-8'))
        serialized_key = online_message.key

        public_key = serialization.load_pem_public_key(bytes(serialized_key, 'utf-8'))
        keys[online_message.name] = public_key

        serialized_keys[online_message.name] = serialized_key
        Path('./serialized_keys.json').write_text(json.dumps(serialized_keys))
    else:
        if serialized_keys[online_message.name] != online_message.key:
            print("Different public keys")
            raise HTTPException(status_code=401, detail="Different public keys")
    
    try:
        keys[online_message.name].verify(
            sig,
            bytes(online_message.message, 'utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
    except Exception:
        print("Error checking signature")
        raise HTTPException(status_code=401, detail="Error checking signature")
    
    online_participants[online_message.name] = uri

print("Starting server")
uvicorn.run(app, host="0.0.0.0", port=5000)
