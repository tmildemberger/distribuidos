from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

participants = ['http://localhost:5001', 'http://localhost:5002']
decision = None

@app.post('/start_transaction')
def start_transaction():
    global decision
    decision = None

    try:
        # Fase 1: Envia a mensagem de voto para os participantes
        for participant in participants:
            response = requests.post(f'{participant}/prepare')
            if response.json().get('vote') != 'YES':
                raise Exception("Transaction aborted by participant")

        # Fase 2: Confirmação ou anulação com base nos votos recebidos
        for participant in participants:
            response = requests.post(f'{participant}/commit')
            if response.json().get('decision') != 'COMMIT':
                raise Exception("Transaction aborted during commit phase")

        decision = 'COMMIT'
        return {'status': 'Transaction committed'}

    except Exception as e:
        decision = 'ABORT'
        raise HTTPException(status_code=400, detail=f'Transaction aborted - {str(e)}')

@app.get('/get_decision')
def get_decision():
    global decision
    if decision is not None:
        return {'decision': decision}
    else:
        return {'decision': 'UNKNOWN'}