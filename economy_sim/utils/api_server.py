import asyncio
import json
import numpy as np
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from stable_baselines3 import PPO
from economy_sim.envs.economy_env import EconomyEnv

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import os
import glob
from pydantic import BaseModel

# Global Simulation State
env = EconomyEnv()
obs, _ = env.reset() # Initialize obs
model = None
is_running = False # Start Paused
simulation_speed = 1.0 # Steps per second (approx)
manual_override = False
manual_action = [0.0, 0.0, 0.0] # [Income Tax, Corp Tax, UBI]

# Model Management
MODELS_DIR = os.path.join(os.path.dirname(__file__), "../../models/ppo")

def load_model_by_name(model_name: str):
    global model
    try:
        path = os.path.join(MODELS_DIR, model_name)
        model = PPO.load(path)
        print(f"Loaded model: {model_name}")
        return True
    except Exception as e:
        print(f"Failed to load model {model_name}: {e}")
        return False

# Initial Load
initial_model_path = os.path.join(MODELS_DIR, "economy_ppo_final")
if os.path.exists(initial_model_path + ".zip"):
    model = PPO.load(initial_model_path)

class LoadModelRequest(BaseModel):
    model_name: str

@app.get("/models")
async def list_models():
    """List all available .zip models in the models directory."""
    files = glob.glob(os.path.join(MODELS_DIR, "*.zip"))
    model_names = [os.path.basename(f).replace(".zip", "") for f in files]
    return {"models": model_names}

@app.post("/load_model")
async def load_model_endpoint(request: LoadModelRequest):
    """Load a specific model by name."""
    success = load_model_by_name(request.model_name)
    if success:
        return {"status": "success", "message": f"Loaded {request.model_name}"}
    else:
        return {"status": "error", "message": "Model not found or invalid"}

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    global is_running, obs, env, simulation_speed, manual_override, manual_action
    
    # Send initial state immediately
    stats = env.agent_manager.get_market_stats()
    await websocket.send_text(json.dumps({
        "step": env.current_step,
        "gdp": float(stats["gdp"]),
        "real_gdp": float(stats["gdp"]), # Initial Real GDP = Nominal
        "unemployment": float(stats["unemployment"]),
        "avg_price": float(stats["avg_price"]),
        "avg_wage": float(stats["avg_wage"]),
        "inflation_rate": 0.0,
        "tax_revenue": float(stats["tax_revenue"]),
        "govt_cash": float(env.agent_manager.govt_cash),
        "subsistence_failures": int(stats["subsistence_failures"]),
        "gini": float(stats["gini"]),
        "action": {"income_tax": 0, "corp_tax": 0, "ubi": 0},
        "firms": [f.get_state() for f in env.agent_manager.firms],
        "households": [h.get_state() for h in env.agent_manager.households]
    }))
    
    try:
        while True:
            # Wait for command from client
            data = await websocket.receive_text()
            command = json.loads(data)
            
            if command["type"] == "START":
                is_running = True
                print("Simulation Resumed")
            elif command["type"] == "STOP":
                is_running = False
                print("Simulation Paused")
            elif command["type"] == "RESET":
                is_running = False
                obs, _ = env.reset()
                print("Simulation Reset")
                # Broadcast initial state immediately
                stats = env.agent_manager.get_market_stats()
                await manager.broadcast(json.dumps({
                    "step": 0,
                    "gdp": float(stats["gdp"]),
                    "real_gdp": float(stats["gdp"]), # Initial Real GDP = Nominal
                    "unemployment": float(stats["unemployment"]),
                    "avg_price": float(stats["avg_price"]),
                    "avg_wage": float(stats["avg_wage"]),
                    "inflation_rate": 0.0,
                    "tax_revenue": float(stats["tax_revenue"]),
                    "govt_cash": float(env.agent_manager.govt_cash),
                    "subsistence_failures": int(stats["subsistence_failures"]),
                    "gini": float(stats["gini"]),
                    "action": {"income_tax": 0, "corp_tax": 0, "ubi": 0},
                    "firms": [f.get_state() for f in env.agent_manager.firms],
                    "households": [h.get_state() for h in env.agent_manager.households]
                }))
            elif command["type"] == "SET_SPEED":
                simulation_speed = float(command["value"])
                print(f"Speed set to {simulation_speed} FPS")
            elif command["type"] == "SET_MANUAL":
                manual_override = command["value"] # True/False
                print(f"Manual Override: {manual_override}")
            elif command["type"] == "UPDATE_ACTION":
                manual_action = [
                    float(command["income_tax"]),
                    float(command["corp_tax"]),
                    float(command["ubi"])
                ]

    except WebSocketDisconnect:
        manager.disconnect(websocket)

async def simulation_loop():
    global obs, is_running, simulation_speed, manual_override, manual_action
    while True:
        # print(f"Loop running. is_running={is_running}") # Debug
        if is_running:
            # 1. Determine Action
            if manual_override:
                action = np.array(manual_action, dtype=np.float32)
            elif model:
                action, _ = model.predict(obs, deterministic=True)
            else:
                action = env.action_space.sample()
            
            # 2. Step Environment
            obs, reward, terminated, truncated, info = env.step(action)
            
            # 3. Get Detailed Stats
            stats = env.agent_manager.get_market_stats()
            
            # 4. Prepare Data Packet
            # Real GDP = Nominal GDP / (Price Index / Base Price)
            # Base Price is 10.0
            price_index = max(0.1, stats["avg_price"]) / 10.0
            real_gdp = stats["gdp"] / price_index

            data = {
                "step": env.current_step,
                "gdp": float(stats["gdp"]),
                "real_gdp": float(real_gdp), # Added
                "unemployment": float(stats["unemployment"]),
                "avg_price": float(stats["avg_price"]),
                "avg_wage": float(stats["avg_wage"]),
                "inflation_rate": 0.0, 
                "tax_revenue": float(stats["tax_revenue"]),
                "govt_cash": float(env.agent_manager.govt_cash), # Added
                "subsistence_failures": int(stats["subsistence_failures"]),
                "gini": float(stats["gini"]),
                "action": {
                    "income_tax": float(action[0]),
                    "corp_tax": float(action[1]),
                    "ubi": float(action[2])
                },
                "firms": [f.get_state() for f in env.agent_manager.firms],
                "households": [h.get_state() for h in env.agent_manager.households] # Added
            }
            
            # 5. Broadcast
            await manager.broadcast(json.dumps(data))
            
            if terminated or truncated:
                obs, _ = env.reset()
                
        # Dynamic Sleep based on Speed
        # If speed is 1.0, sleep 1.0s. If speed is 60.0, sleep 0.016s.
        sleep_time = 1.0 / max(0.1, simulation_speed)
        await asyncio.sleep(sleep_time)

@app.on_event("startup")
async def startup_event():
    # Don't auto-start simulation loop logic, wait for START command
    # But we need the loop running to check 'is_running' flag
    asyncio.create_task(simulation_loop())

def run_server():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    run_server()
