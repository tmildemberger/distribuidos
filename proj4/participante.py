# bibliotecas do python
import json
from pydantic import BaseModel, Field, Base64Bytes, PositiveInt
from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException
import requests
import base64
import shutil
import threading
import uvicorn
import time
from uuid import uuid4

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
porta = int(part_obj['porta'])

if not Path("./key").exists() or not Path("./key.pub").exists() or not Path("./shards.json").exists()or not Path("./servers.json").exists():
    import sys
    print("Participante não foi inicializado corretamente")
    sys.exit("Participante não foi inicializado corretamente")

public_key = serialization.load_pem_public_key(bytes(Path("./key.pub").read_text(), 'utf-8'))
private_key = serialization.load_pem_private_key(bytes(Path("./key").read_text(), 'utf-8'), password=None)

servers_obj = json.loads(Path("./servers.json").read_text())
shards_obj = json.loads(Path("./shards.json").read_text())

vote = 'YES'

################################################################################
mod_overrides_start = """return {
  ["workshop-1185229307"]={
    configuration_options={
      CAMERA=true,
      DAMAGE_NUMBERS=true,
      DAMAGE_RESISTANCE=false,
      FRAME_PHASES=true,
      GLOBAL=false,
      GLOBAL_NUMBERS=false,
      HEADER_CLIENT=false,
      HEADER_SERVER=false,
      HORIZONTAL_OFFSET=0,
      TAG="EPIC",
      WETNESS_METER=false 
    },
    enabled=true 
  },
  ["workshop-1378549454"]={
    configuration_options={
      ["MemSpikeFix:"]=false,
      MemSpikeFixmaster_override=true,
      ["MemSpikeFixworkshop-1185229307"]="default",
      ["MemSpikeFixworkshop-1467214795"]="default",
      ["MemSpikeFixworkshop-351325790"]="default",
      craftinghighlight=false 
    },
    enabled=true 
  },
  ["workshop-1467214795"]={
    configuration_options={
      ["4 Shard Dedicated Servers"]=false,
      ["Character Refreshes"]=false,
      ["Cut Content Restoration"]=false,
      ["Gameplay Features"]=false,
      ["Items & Structures"]=false,
      ["Misc."]=false,
      Mobs=false,
      devmode=false,
      droplootground=true,
      dynamicmusic=true,
      leif_jungle=false,
      limestonerepair=true,
      locale=false,
      newloot="all",
      newplayerboats=true,
      octopuskingtweak=true,
      octopustrade=true,
      oldwarly=false,
      pondfishable=true,
      quickseaworthy=false,
      slotmachineloot=true,
      tuningmodifiers=true,
      windgustable="all","""

mod_overrides_end = """\n      windstaffbuff=2 
    },
    enabled=true 
  } 
}"""
################################################################################




coordinator_uri = 'http://localhost:5000'

class OnlineParticipantMsg(BaseModel):
    name: str
    message: str
    signature: str

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

mensagem = f'http://localhost:{porta}'
mensagem_bytes = bytes(mensagem, 'utf-8')
assinatura = private_key.sign(
    mensagem_bytes,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
}


#######
@app.post('/prepare')
def prepare(transaction: Transaction):
    try:
        if Path("./status").exists():
            raise Exception("Currently in transaction")
        
        global vote
        #Guardar todas as informações necessárias antes de dar o voto
        here = False
        for shard in transaction.description:
            if shard.where == nome:
                here = True
                break
        
        new_server = {
            "id": transaction.transaction_id,
            "name": transaction.server_name,
            "shards": [shard.shard_id for shard in transaction.description]
        }

        if here:
            server_folder = Path(f"./{transaction.server_name}")
            if server_folder.exists():
                print("Error: server already exists?")
                vote = 'NO'
                return {'vote': vote}
            
            server_folder.mkdir()

        mod_overrides = mod_overrides_start
        for shard in transaction.description:
            if shard.shard_generator == 'Forest':
                mod_overrides += f"\n      forestid=\"{shard.shard_index}\","
            elif shard.shard_generator == 'Caves':
                mod_overrides += f"\n      cavesid=\"{shard.shard_index}\","
            elif shard.shard_generator == 'Islands':
                mod_overrides += f"\n      shipwreckedid=\"{shard.shard_index}\","
            elif shard.shard_generator == 'Volcano':
                mod_overrides += f"\n      volcanoid=\"{shard.shard_index}\","
        mod_overrides += mod_overrides_end

        new_shards = []

        for shard in transaction.description:
            if shard.where == nome:
                new_shard = {
                    "id": shard.shard_id,
                    "name": shard.name,
                    "type": shard.shard_type,
                    "server_name": transaction.server_name
                }
                new_shards.append(new_shard)

                (server_folder / shard.name).mkdir()
                (server_folder / shard.name / 'modoverrides.lua').write_text(mod_overrides)
                server_ini = f"""[NETWORK]
server_port = {11000 + shard.shard_index}


[SHARD]
is_master = {"true" if shard.shard_type == "Master" else "false"}
name = {shard.name}
id = {shard.shard_index}


[STEAM]
master_server_port = 27018
authentication_port = 8768


[ACCOUNT]
encode_user_path = true
"""
                (server_folder / shard.name / 'server.ini').write_text(server_ini)

                if shard.shard_generator == 'Forest':
                    (server_folder / shard.name / 'worldgenoverride.lua').write_text(
                        (Path('../shard_generators') / 'forest_worldgenoverride.lua').read_text()
                    )
                elif shard.shard_generator == "Caves":
                    (server_folder / shard.name / 'worldgenoverride.lua').write_text(
                        (Path('../shard_generators') / 'caves_worldgenoverride.lua').read_text()
                    )
                elif shard.shard_generator == "Islands":
                    (server_folder / shard.name / 'worldgenoverride.lua').write_text(
                        (Path('../shard_generators') / 'islands_worldgenoverride.lua').read_text()
                    )
                elif shard.shard_generator == "Volcano":
                    (server_folder / shard.name / 'worldgenoverride.lua').write_text(
                        (Path('../shard_generators') / 'volcano_worldgenoverride.lua').read_text()
                    )



        prepared_servers_obj = json.loads(Path("./servers.json").read_text())
        prepared_shards_obj = json.loads(Path("./shards.json").read_text())

        prepared_servers_obj.append(new_server)
        for ns in new_shards:
            prepared_shards_obj.append(ns)

        Path("./prepared_servers.json").write_text(json.dumps(prepared_servers_obj, indent=4))
        Path("./prepared_shards.json").write_text(json.dumps(prepared_shards_obj, indent=4))

        Path("./status").write_text(json.dumps(transaction.transaction_id, indent=4))

        vote = 'YES'
        return {'vote': vote}
    
    except Exception as e:
        vote = 'NO'
        return {'vote': vote}


# @app.get('/public_key')
# def public_key():
#     ret = Path("./key.pub").read_text()
#     print(ret)
#     return ret

@app.post('/commit')
def commit(transaction: Transaction):
    #Commitar caso o coordenador tenha a decision de commit 
    if transaction.status == 'Prepared':
        
        Path("./prepared_servers.json").replace(Path("./servers.json"))
        Path("./prepared_shards.json").replace(Path("./shards.json"))
        Path("./status").unlink()

        return {'decision':'COMMIT'}
    else:
        Path("./prepared_servers.json").unlink()
        Path("./prepared_shards.json").unlink()
        Path("./status").unlink()

        server_folder = Path(f"./{transaction.server_name}")
        if server_folder.exists():
            shutil.rmtree(server_folder)

        return {'decision':'ABORT'}

# inicia thread em background para a api
th = threading.Thread(target=uvicorn.run, args=(app,), kwargs={'host':"0.0.0.0", 'port':porta})
th.daemon = True
th.start()
# uvicorn.run(app, host="0.0.0.0", port=porta)

# online_message = OnlineParticipantMsg(name=nome, message=mensagem)#, signature=base64.encodebytes(assinatura))
online_message = {'name':nome, 'message':mensagem, 'signature':base64.encodebytes(assinatura).decode('ascii'), 'key': Path("./key.pub").read_text()}

response = requests.post(f'{coordinator_uri}/online', json=online_message)
if response.status_code not in [201, 200]:
    print(response.text)
    raise Exception("Coordinator seems offline")

# ver log e ver se tem transação em aberto
if Path("./status").exists():
    transaction_id = json.loads(Path("./status").read_text())
    response = requests.get(f'{coordinator_uri}/transactions/{transaction_id}')
    if response.status_code not in [201, 200]:
        raise Exception("Unknown error")
    transaction = response.json()
    if transaction['status'] == "Committed":
        Path("./prepared_servers.json").replace(Path("./servers.json"))
        Path("./prepared_shards.json").replace(Path("./shards.json"))
        Path("./status").unlink()
    elif transaction['status'] == "Aborted":
        Path("./prepared_servers.json").unlink()
        Path("./prepared_shards.json").unlink()
        Path("./status").unlink()

        server_folder = Path(f"./{transaction['server_name']}")
        if server_folder.exists():
            shutil.rmtree(server_folder)
    else:
        raise Exception("Unknown transaction status")

while True:
    time.sleep(60)
    # ver log e ver se tem transação em aberto
    if Path("./status").exists():
        transaction_id = json.loads(Path("./status").read_text())
        response = requests.get(f'{coordinator_uri}/transactions/{transaction_id}')
        if response.status_code not in [201, 200]:
            raise Exception("Unknown error")
        transaction = response.json()
        if transaction['status'] == "Committed":
            Path("./prepared_servers.json").replace(Path("./servers.json"))
            Path("./prepared_shards.json").replace(Path("./shards.json"))
            Path("./status").unlink()
        elif transaction['status'] == "Aborted":
            Path("./prepared_servers.json").unlink()
            Path("./prepared_shards.json").unlink()
            Path("./status").unlink()

            server_folder = Path(f"./{transaction['server_name']}")
            if server_folder.exists():
                shutil.rmtree(server_folder)
        else:
            raise Exception("Unknown transaction status")
