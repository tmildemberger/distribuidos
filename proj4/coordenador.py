from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel, Field, Base64Bytes
from uuid import uuid4
from pathlib import Path

import requests

# biblioteca cryptography para assinatura e verificação com chaves rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, utils, padding

app = FastAPI()

def _find_next_id():
    return str(uuid4())

class Shard(BaseModel):
    shard_id: Field(default_factory=_find_next_id, alias='id')
    where: str
    name: str
    shard_type: str
    server_name: str

class Transaction(BaseModel):
    transaction_id: Field(default_factory=_find_next_id, alias='id')
    status: str
    description: List[Shard]


class OnlineParticipantMsg(BaseModel):
    name: str
    message: str
    signature: Base64Bytes

if not Path('./coordinator.json').exists():
    import sys
    print("Coordinator not initialized")
    sys.exit("Coordinator not initialized")

if not Path('./serialized_keys.json').exists():
    Path('./serialized_keys.json').write_text(json.dumps({}))

transactions = dict()
serialized_keys = json.loads(Path('./serialized_keys.json').read_text())
keys = {k: serialization.load_pem_public_key(bytes(v, 'utf-8')) for k,v in serialized_keys.items()}
online_participants = dict()

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
    transaction.status = 'Open'
    transactions[transaction.id] = transaction
    return transaction

@app.post("/online")
async def post_online(online_message: OnlineParticipantMsg):
    uri = online_message.message
    if online_message.name not in keys.keys():
        resp = requests.get(uri + '/public_key')
        if resp.status != 201:
            print("No public key")
            raise HTTPException(status_code=401, detail="No public key")
        public_key = serialization.load_pem_public_key(bytes(resp.json()['key'], 'utf-8'))
        keys[online_message.name] = public_key
    
    try:
        keys[online_message.name].verify(
            online_message.signature.base64_bytes,
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


