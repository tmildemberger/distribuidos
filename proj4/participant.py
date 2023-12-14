from fastapi import FastAPI

app = FastAPI()

vote = None

@app.post('/prepare')
def prepare():
    global vote
    # Lógica para verificar se o participante está pronto para a transação
    # Pode incluir verificação de recursos, validação de dados, etc.

    # Simplesmente vota 'YES' para este exemplo
    vote = 'YES'
    return {'vote': vote}

@app.get('/commit')
def commit():
    global vote
    # Lógica para efetivar a transação se o participante votou 'YES'
    # Pode incluir a confirmação da criação do mundo ou a reversão em caso de falha

    if vote == 'YES':
        # Lógica para confirmar a transação
        return {'decision': 'COMMIT'}
    else:
        # Lógica para reverter a transação
        return {'decision': 'ABORT'}