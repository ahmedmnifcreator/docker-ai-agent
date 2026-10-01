from fastapi import FastAPI

app = FastAPI(
    title="Docker AI Agent",
    description="Autonomous agent for containerizing projects",
    version="1.0.0"
)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "docker-ai-agent"
    }