from fastapi import FastAPI

app = FastAPI(title="Syscora API", description="API pour l'application de comptabilité analytique Syscora")

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API Syscora"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
