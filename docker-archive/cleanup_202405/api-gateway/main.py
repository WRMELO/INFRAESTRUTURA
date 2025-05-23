from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="API Gateway",
    description="Ponto de entrada para todos os micro‑serviços",
    version="0.1.0"
)

# Habilitar CORS (ajuste as origens conforme sua segurança)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Health"])
async def health_check():
    """
    Health check simples.
    """
    return {"status": "ok", "service": "api-gateway"}

# Exemplo de rota que delega para outro serviço
@app.get("/proxy/{service_name}", tags=["Proxy"])
async def proxy(service_name: str):
    """
    Aqui você poderia realizar um request interno,
    por exemplo com httpx, para o serviço dado.
    """
    return {"message": f"Você pediu o serviço {service_name}"}
