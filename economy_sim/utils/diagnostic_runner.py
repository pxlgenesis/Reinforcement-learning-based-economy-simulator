import os
import sys
import time
import numpy as np
from economy_sim.envs.economy_env import EconomyEnv

def run_diagnostic(steps=200):
    """
    Runs the economy simulation headlessly and logs detailed metrics to 3 separate files.
    """
    print(f"Starting Diagnostic Run for {steps} steps...")
    
    env = EconomyEnv()
    obs, _ = env.reset()
    
    # Open 3 files
    f_macro = open("diagnostic_macro.txt", "w")
    f_firms = open("diagnostic_firms.txt", "w")
    f_house = open("diagnostic_households.txt", "w")
    
    # Headers
    f_macro.write(f"Diagnostic Run Start: {time.ctime()}\n")
    f_macro.write("Step | GDP | Inflation | Unemp | GovtCash | AvgPrice | AvgWage | Tiers(1/2/3/4) | Monopolies\n")
    f_macro.write("-" * 120 + "\n")
    
    f_firms.write(f"Diagnostic Run Start: {time.ctime()}\n")
    f_firms.write("Step | ID | Tier | Cash | Emp/Max | Wage | Price | Inv | Profit\n")
    f_firms.write("-" * 100 + "\n")
    
    f_house.write(f"Diagnostic Run Start: {time.ctime()}\n")
    f_house.write("Step | ID | Cash | Skill | Emp? | Wage | ResWage | Contract\n")
    f_house.write("-" * 100 + "\n")
    
    try:
        for step in range(steps):
            # Action: Fixed "Hands Off" policy (0.2 tax, 0 UBI)
            action = np.array([0.2, 0.2, 0.0], dtype=np.float32)
            
            obs, reward, done, truncated, info = env.step(action)
            manager = env.agent_manager
            
            # --- Macro Log ---
            gdp = manager.gdp
            unemp = manager.unemployment_rate
            govt_cash = manager.govt_cash
            avg_price = manager.avg_price
            avg_wage = manager.avg_wage
            
            tiers = [0, 0, 0, 0]
            for firm in manager.firms:
                if 1 <= firm.tier <= 4:
                    tiers[firm.tier - 1] += 1
            
            total_employed = sum([len(f.employees) for f in manager.firms])
            max_share = 0.0
            if total_employed > 0:
                max_emp = max([len(f.employees) for f in manager.firms])
                max_share = max_emp / total_employed
            
            log_line = (f"{step:4d} | ${gdp:10.2f} | {avg_price:10.2f} | {unemp:5.1%} | "
                        f"${govt_cash:10.2f} | ${avg_wage:8.2f} | "
                        f"{tiers[0]}/{tiers[1]}/{tiers[2]}/{tiers[3]} | {max_share:5.1%}")
            f_macro.write(log_line + "\n")
            
            if step % 20 == 0:
                print(log_line)
            
            # --- Firms Log (Snapshot every 10 steps to save space) ---
            if step % 10 == 0:
                for f in manager.firms:
                    f_line = (f"{step:4d} | {f.id:2d} | T{f.tier} | ${f.cash:9.0f} | "
                              f"{len(f.employees):3d}/{f.max_employees:3d} | ${f.wage_offer:7.2f} | "
                              f"${f.price:7.2f} | {f.inventory:5.0f} | ${f.last_profit:8.0f}")
                    f_firms.write(f_line + "\n")
                f_firms.write("-" * 50 + "\n")

            # --- Households Log (Snapshot every 20 steps) ---
            if step % 20 == 0:
                # Log first 10 households only to keep file size manageable
                for h in manager.households[:10]: 
                    h_line = (f"{step:4d} | {h.id:2d} | ${h.cash:8.0f} | {h.skill:5.2f} | "
                              f"{'YES' if h.is_employed else 'NO '} | ${h.wage:7.2f} | "
                              f"${h.reservation_wage:7.2f} | {h.contract_remaining}mo")
                    f_house.write(h_line + "\n")
                f_house.write("-" * 50 + "\n")
                
            if done or truncated:
                print("Simulation ended early.")
                break
                
    finally:
        f_macro.close()
        f_firms.close()
        f_house.close()

    print(f"\nDiagnostic Run Complete.")
    print("Logs saved: diagnostic_macro.txt, diagnostic_firms.txt, diagnostic_households.txt")

if __name__ == "__main__":
    run_diagnostic()
