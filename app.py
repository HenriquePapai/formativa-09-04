from fastapi import FastAPI, Request
from pydantic import BaseModel
import database
from log import LOGGER

class LoginSchema(BaseModel):
    usuario: str
    senha: str

API = FastAPI()

database.criar_banco()

def log_info(req: Request, mensagem: str):
    extra = {"endpoint": req.url.path, "ip": req.client.host}
    LOGGER.info(mensagem, extra=extra)

@API.get("/health")
def health(request: Request):
    database.incrementar_metrica("total_requests")
    log_info(request, "Check de saude realizado")
    return {"status": "OK"}

@API.post("/login")
def login(dados: LoginSchema, request: Request):
    database.incrementar_metrica("total_requests")

    if database.verificar_login(dados.usuario, dados.senha):
        log_info(request, "Login sucesso: " + dados.usuario)
        return {"status": "Sucesso", "usuario": dados.usuario}
    
    database.incrementar_metrica("failed_logins")
    log_info(request, "Falha login: " + dados.usuario)
    return {"status": "Erro", "detalhe": "Incorreto"}

@API.get("/metricas")
def get_metricas(request: Request):
    database.incrementar_metrica("total_requests")
    log_info(request, "Consulta de metricas")
    return database.obter_metricas()