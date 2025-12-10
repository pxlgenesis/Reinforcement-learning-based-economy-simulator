import os
import sys
import numpy as np
from economy_sim.envs.economy_env import EconomyEnv
from economy_sim.config import N_FIRMS, N_HOUSEHOLDS

def run_stability_check(steps=240, output_file="stability_report.txt"):
    """
    Runs the simulation for a specified number of steps and logs key metrics.
    """
    env = EconomyEnv()
    obs, _ = env.reset()
    
    print(f"Starting Stability Check for {steps} steps (20 Years)...")
    
    with open(output_file, "w") as f:
        f.write("=== Economy Simulation Stability Report ===\n")
        f.write(f"Simulation Duration: {steps} Months\n")
        f.write(f"Agents: {N_FIRMS} Firms, {N_HOUSEHOLDS} Households\n\n")
        
        # Trackers
        history = {
            "unemployment": [],
            "avg_price": [],
            "avg_wage": [],
            "gdp": [],
            "firm_cash": [],
            "household_cash": [],
            "firm_tiers": [],
            "bankruptcies": 0
        }
        
        for step in range(steps):
            # Use a dummy action (e.g., no tax changes) or random
            # Action space: [Income Tax, Corp Tax, UBI]
            # Let's keep taxes low/stable to test organic stability
            action = np.array([0.1, 0.1, 0.0], dtype=np.float32) 
            
            obs, reward, done, truncated, info = env.step(action)
            
            # Extract Metrics from Agent Manager
            manager = env.agent_manager
            stats = manager.get_market_stats()
            
            # Record Data
            history["unemployment"].append(stats["unemployment"])
            history["avg_price"].append(stats["avg_price"])
            history["avg_wage"].append(stats["avg_wage"])
            history["gdp"].append(stats["gdp"])
            
            avg_firm_cash = np.mean([firm.cash for firm in manager.firms])
            avg_hh_cash = np.mean([h.cash for h in manager.households])
            avg_tier = np.mean([firm.tier for firm in manager.firms])
            
            history["firm_cash"].append(avg_firm_cash)
            history["household_cash"].append(avg_hh_cash)
            history["firm_tiers"].append(avg_tier)
            
            # Count bankruptcies in this step (cumulative check)
            # Actually, manager tracks total bankruptcies? No, firm tracks it.
            # We can check how many firms reset this step.
            # Simplified: just track total at end.
            
            if step % 12 == 0:
                print(f"Year {step//12}: Unemp={stats['unemployment']:.2f}, Price={stats['avg_price']:.2f}, Wage={stats['avg_wage']:.2f}, Tier={avg_tier:.2f}")

        # --- Analysis ---
        f.write("=== Final Statistics ===\n")
        f.write(f"Final Unemployment: {history['unemployment'][-1]*100:.1f}%\n")
        f.write(f"Final Avg Price: ${history['avg_price'][-1]:.2f}\n")
        f.write(f"Final Avg Wage: ${history['avg_wage'][-1]:.2f}\n")
        f.write(f"Final GDP: ${history['gdp'][-1]:.2f}\n")
        f.write(f"Final Avg Firm Cash: ${history['firm_cash'][-1]:.2f}\n")
        f.write(f"Final Avg Household Cash: ${history['household_cash'][-1]:.2f}\n")
        f.write(f"Final Avg Firm Tier: {history['firm_tiers'][-1]:.2f}\n")
        
        total_bankruptcies = sum([firm.bankruptcies for firm in manager.firms])
        f.write(f"Total Firm Bankruptcies: {total_bankruptcies}\n")
        
        # --- Stability Checks ---
        f.write("\n=== Stability Analysis ===\n")
        
        # 1. Employment Check
        avg_unemp = np.mean(history["unemployment"])
        if avg_unemp > 0.5:
            f.write("[FAIL] High Unemployment: Average > 50%\n")
        elif avg_unemp < 0.05:
            f.write("[WARN] Low Unemployment: Average < 5% (Labor Shortage?)\n")
        else:
            f.write("[PASS] Employment Levels Healthy\n")
            
        # 2. Inflation Check
        start_price = history["avg_price"][0]
        end_price = history["avg_price"][-1]
        inflation = (end_price - start_price) / start_price if start_price > 0 else 0
        f.write(f"Total Inflation (20 Years): {inflation*100:.1f}%\n")
        if inflation > 50.0: # Hyperinflation
             f.write("[WARN] High Inflation detected.\n")
        elif inflation < -0.5:
             f.write("[FAIL] Deflationary Spiral detected.\n")
        else:
             f.write("[PASS] Price Stability Acceptable\n")
             
        # 3. Firm Growth Check
        if history["firm_tiers"][-1] <= 1.1:
            f.write("[FAIL] Stagnation: Firms are not upgrading Tiers.\n")
        else:
            f.write("[PASS] Economic Growth: Firms are upgrading.\n")
            
        # 4. Wealth Distribution
        if history["household_cash"][-1] < 100:
             f.write("[FAIL] Poverty: Households are broke.\n")
        else:
             f.write("[PASS] Household Wealth exists.\n")

    print(f"Stability Check Complete. Report saved to {output_file}")

if __name__ == "__main__":
    run_stability_check()
