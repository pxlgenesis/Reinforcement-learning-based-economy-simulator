import numpy as np
from economy_sim.config import (
    INITIAL_CASH_FIRM,
    AVG_PRODUCTIVITY,
    PRICE_STICKINESS,
    HIRING_BUFFER_MONTHS,
    INVENTORY_DEPRECIATION,
    WAGE_FLOOR
)

# Tier Definitions
# Level: (Max Employees, Upgrade Cost, Fixed Overhead)
TIER_CONFIG = {
    1: {"max_emp": 5, "cost": 0, "overhead": 0},
    2: {"max_emp": 20, "cost": 20000, "overhead": 200},
    3: {"max_emp": 50, "cost": 100000, "overhead": 2000},
    4: {"max_emp": 200, "cost": 500000, "overhead": 10000}
}

class Firm:
    def __init__(self, agent_id: int):
        self.id = agent_id
        self.cash = INITIAL_CASH_FIRM
        self.inventory = 0.0
        self.price = 10.0  # Initial price guess
        self.wage_offer = 100.0 # Initial wage offer
        self.employees = [] # List of Household IDs
        self.bankruptcies = 0 # Track failure count
        self.failed_to_hire = False # Flag: Did we try to hire but failed?
        
        # Tier System
        self.tier = 1
        self.max_employees = TIER_CONFIG[1]["max_emp"]
        
        # Metrics
        self.last_profit = 0.0
        self.last_production = 0.0
        self.last_sales = 0.0
        self.total_sales_revenue = 0.0
        self.starting_cash = self.cash # Track cash at start of step for profit calc

    def step(self):
        """
        Monthly update loop.
        1. Pay Overhead (Tier Maintenance).
        2. Attempt Upgrade (Growth).
        3. Depreciate inventory.
        4. Adjust Prices (Sticky).
        5. Adjust Wages (Hiring Budget).
        6. Check Bankruptcy.
        """
        # 0. Pay Fixed Overhead (Infrastructure Cost)
        overhead = TIER_CONFIG[self.tier]["overhead"]
        # Scale overhead with price to prevent it becoming irrelevant in inflation
        # Use self.price as a proxy for general price level
        # Dampen scaling (Square Root) to prevent overheads from killing firms during inflation
        price_ratio = max(1.0, self.price / 10.0)
        scaled_overhead = overhead * (price_ratio ** 0.5) 
        self.cash -= scaled_overhead

        # 1. Attempt Upgrade
        self._attempt_upgrade()

        # 2. Depreciation (Rot)
        self.inventory *= (1.0 - INVENTORY_DEPRECIATION)
        
        # 3. Pricing Logic (Supply/Demand)
        target_price = self.price
        safe_last_sales = max(self.last_sales, 0.1)
        
        if self.inventory > safe_last_sales * 2:
            target_price = self.price * 0.95
        elif self.inventory < safe_last_sales * 0.25:
            # Only raise price if we actually have goods to sell or produced something
            # If we produced 0, raising price is useless (we have nothing to ration)
            if self.last_production > 0 or self.inventory > 0:
                target_price = self.price * 1.05
            else:
                # We have nothing. Lower price to signal "we are broken" or stay same?
                # Actually, if we have nothing, price is theoretical. 
                # But high price prevents future sales if we do produce.
                # Let's decay price slowly to reset market expectations.
                target_price = self.price * 0.98
            
        # Apply Stickiness
        change = np.clip(target_price - self.price, -self.price * PRICE_STICKINESS, self.price * PRICE_STICKINESS)
        self.price += change
        self.price = max(0.1, self.price) # Price floor

        # 4. Wage/Hiring Logic
        can_afford_hire = self.cash > (self.wage_offer * HIRING_BUFFER_MONTHS)
        at_capacity = len(self.employees) >= self.max_employees
        
        # Calculate Sustainable Wage (Revenue per worker)
        # Production ~ AVG_PRODUCTIVITY (diminishing returns ignored for simplicity of estimation)
        sustainable_wage = (self.price * AVG_PRODUCTIVITY) * 0.9
        
        if self.failed_to_hire:
            # Only raise if we are below sustainable levels
            if self.wage_offer < sustainable_wage:
                self.wage_offer *= 1.10 
            else:
                # We can't afford to pay more, so we must wait or lower price to sell more volume?
                # Actually, if we can't hire at sustainable wage, we are inefficient.
                pass 
        elif self.last_profit > 0 and can_afford_hire and not at_capacity:
            self.wage_offer *= 1.02 
        elif self.last_profit < 0:
            self.wage_offer *= 0.98 
            
        # Hard Cap to prevent death spirals
        self.wage_offer = min(self.wage_offer, sustainable_wage)
        self.wage_offer = max(WAGE_FLOOR, self.wage_offer)
        self.failed_to_hire = False 

        # 5. Bankruptcy Check
        # Return True if bankrupt, Manager handles the rest
        if self.cash < 0:
            return True
        return False

    def _attempt_upgrade(self):
        """
        Check if we can afford to upgrade to the next tier.
        """
        if self.tier >= 4: return
        
        next_tier = self.tier + 1
        cost = TIER_CONFIG[next_tier]["cost"]
        # Scale cost with inflation, but damp it significantly (Fourth Root)
        # If Price is 10x (100.0), cost is 1.77x.
        # This allows firms to catch up to inflation.
        price_ratio = max(1.0, self.price / 10.0)
        scaled_cost = cost * (price_ratio ** 0.25)
        
        if self.cash > scaled_cost * 1.5:
            self.cash -= scaled_cost
            self.tier = next_tier
            self.max_employees = TIER_CONFIG[next_tier]["max_emp"]
            # print(f"Firm {self.id} upgraded to Tier {self.tier}!")

    def produce_goods(self, total_skill_input: float):
        """
        Production = Productivity * (Total Skill Input ^ 0.9)
        """
        production = AVG_PRODUCTIVITY * (total_skill_input ** 0.9)
        self.inventory += production
        self.last_production = production

    def _restructure(self, bailout_amount: float = INITIAL_CASH_FIRM):
        """
        Bankruptcy logic: Reset the firm.
        """
        self.bankruptcies += 1
        
        self.cash = bailout_amount
        self.inventory = 0.0
        self.employees = [] 
        self.last_profit = 0.0
        
        # Reset Tier to 1 (Startup)
        self.tier = 1
        self.max_employees = TIER_CONFIG[1]["max_emp"]
        
        # Soft Reset Price/Wage
        self.price = max(10.0, self.price * 0.8) 
        self.wage_offer = max(WAGE_FLOOR, self.wage_offer * 0.8)
        self.total_sales_revenue = 0.0

    def get_state(self):
        return {
            "id": int(self.id),
            "cash": float(self.cash),
            "inventory": float(self.inventory),
            "price": float(self.price),
            "wage_offer": float(self.wage_offer),
            "employees_count": int(len(self.employees)),
            "bankruptcies": int(self.bankruptcies),
            "last_profit": float(self.last_profit),
            "tier": int(self.tier), # Added
            "max_employees": int(self.max_employees) # Added
        }
