from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Data Processing Service",
    description="API para processamento de dados (pandas, sklearn…) ",
    version="0.1.0"
)

# CORS básico
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "service": "data-processing"}

# Exemplo de endpoint de processamento
@app.get("/process", tags=["Process"])
async def process_sample():
    """
    Endpoint de exemplo que retornaria resultados de um job pandas/sklearn.
    """
    return {"message": "Processamento funcionando!"}
