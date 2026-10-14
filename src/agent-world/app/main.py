import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.engine import AgentWorldEngine

app = FastAPI(title="RiskTwin Agent World API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = AgentWorldEngine(backend_url="http://localhost:5000")
simulation_task = None

async def simulation_loop():
    while engine.is_running:
        await engine.step()
        await asyncio.sleep(engine.tick_speed)

@app.get("/api/world/status")
async def get_status():
    return {
        "is_running": engine.is_running,
        "tick_speed": engine.tick_speed,
        "agents_count": len(engine.agents),
        "total_events": len(engine.live_logs)
    }

@app.get("/api/world/agents")
async def get_agents():
    return [a.to_dict() for a in engine.agents]

@app.get("/api/world/events")
async def get_events():
    return engine.live_logs

@app.post("/api/world/start")
async def start_simulation(speed: float = 2.5):
    global simulation_task
    engine.tick_speed = max(0.5, speed)
    if not engine.is_running:
        engine.is_running = True
        simulation_task = asyncio.create_task(simulation_loop())
    return {"status": "started", "speed": engine.tick_speed}

@app.post("/api/world/pause")
async def pause_simulation():
    engine.is_running = False
    return {"status": "paused"}

@app.post("/api/world/step")
async def single_step(agent_id: str = None):
    event = await engine.step(agent_id=agent_id)
    return {"status": "stepped", "event": event}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)
