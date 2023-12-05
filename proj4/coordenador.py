from fastapi import FastAPI
from pydantic import BaseModel, Field
from uuid import uuid4

app = FastAPI()

def _find_next_id():
    return str(uuid4())

class Transaction(BaseModel):
    transaction_id: Field(default_factory=_find_next_id, alias='id')
    status: str



transactions = []

@app.get("/transactions")
async def get_transactions():
    return transactions

@app.post("transactions")
async def post_transaction(transaction: Transaction):
    transaction.status = 'Open'
    transactions.append(transaction)
    return transaction