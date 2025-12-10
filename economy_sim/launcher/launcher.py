import argparse
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    parser = argparse.ArgumentParser(description="Economy Simulation Launcher")
    parser.add_argument("--train", action="store_true", help="Train the RL Agent")
    parser.add_argument("--sim", action="store_true", help="Run the Simulation with Dashboard")
    parser.add_argument("--test", action="store_true", help="Run a quick smoke test")
    
    args = parser.parse_args()
    
    if args.train:
        print("Starting RL Training...")
        from economy_sim.training.train_ppo import train
        train()
        
    elif args.sim:
        print("Starting Economy Simulation Stack...")
        
        import subprocess
        import time
        import os
        import signal
        import sys

        # 1. Start Backend
        print(">> Launching Backend (FastAPI)...")
        backend = subprocess.Popen(
            [sys.executable, "-m", "economy_sim.utils.api_server"],
            cwd=os.getcwd(),
            env=os.environ.copy()
        )
        
        # 2. Start Frontend
        print(">> Launching Frontend (Next.js)...")
        frontend = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=os.path.join(os.getcwd(), "frontend"),
            shell=True
        )

        print("\nStack is running!")
        print("Backend: http://localhost:8000")
        print("Frontend: http://localhost:3000")
        print("Press Ctrl+C to stop.\n")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down...")
            backend.terminate()
            # Frontend (npm) is harder to kill on Windows via shell=True, but this is a start
            if os.name == 'nt':
                subprocess.call(['taskkill', '/F', '/T', '/PID', str(frontend.pid)])
            else:
                frontend.terminate()
            sys.exit(0)
        
    elif args.test:
        print("Running Smoke Test...")
        # We can import the test logic here or run the script
        import subprocess
        subprocess.run(["python", "test_simulation.py"])
        
    else:
        print("Please specify an action: --train, --sim, or --test")

if __name__ == "__main__":
    main()
