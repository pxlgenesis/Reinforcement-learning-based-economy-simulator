import numpy as np
from economy_sim.config import (
    SUBSISTENCE_COST, 
    WAGE_FLOOR, 
    INITIAL_CASH_HOUSEHOLD
)

class Household:
    def __init__(self, agent_id: int, skill_level: float = 1.0):
        self.id = agent_id
        self.cash = INITIAL_CASH_HOUSEHOLD
        self.skill = skill_level
        self.inventory = 0.0
        self.employer_id = None
        self.wage = 0.0
        self.reservation_wage = WAGE_FLOOR
        self.is_employed = False
        self.months_unemployed = 0
        self.contract_remaining = 0 # Months left on contract
        
        # Metrics for dashboard
        self.last_consumption = 0.0
        self.subsistence_failed = False

    def step(self, inflation_rate: float = 0.0):
        """
        Daily/Monthly update loop.
        1. Consume goods (Survival).
        2. Update Skill (Experience/Decay).
        3. Adjust Reservation Wage (COLA + Market Dynamics).
        """
        # 1. Consumption Logic
        self._consume()
        
        # 2. Skill Dynamics
        if self.is_employed:
            self.skill *= 1.001  # +0.1% per month (~1.2% per year)
            self.months_unemployed = 0
            if self.contract_remaining > 0:
                self.contract_remaining -= 1
        else:
            self.months_unemployed += 1
            if self.months_unemployed > 12:
                self.skill *= 0.999  # Atrophy if long-term unemployed

        # 3. Reservation Wage Adjustment
        # Base adjustment: Cost of Living Adjustment (COLA)
        # If inflation is positive, raise reservation wage to keep up.
        if inflation_rate > 0:
            self.reservation_wage *= (1.0 + inflation_rate)

        # Market Dynamics
        # If unemployed for long, lower standards aggressively
        if not self.is_employed:
            if self.months_unemployed > 6:
                self.reservation_wage = max(WAGE_FLOOR, self.reservation_wage * 0.90) # -10% per month
            elif self.months_unemployed > 3:
                self.reservation_wage = max(WAGE_FLOOR, self.reservation_wage * 0.98) # -2% per month
        
        # If employed and saving money, raise standards
        if self.is_employed and self.cash > SUBSISTENCE_COST * 6:
            self.reservation_wage *= 1.02

    def _consume(self):
        """
        Consume 1 unit of inventory for survival.
        If inventory < 1, flag subsistence_failed.
        Also implement spoilage/cap: Max inventory is 24 months (24.0).
        """
        # 1. Spoilage / Cap Check
        MAX_INVENTORY = 24.0
        if self.inventory > MAX_INVENTORY:
            self.inventory = MAX_INVENTORY

        # 2. Consumption
        if self.inventory >= 1.0:
            self.inventory -= 1.0
            self.subsistence_failed = False
        else:
            # Starvation / Poverty event
            self.inventory = 0.0
            self.subsistence_failed = True

    def get_state(self):
        return {
            "id": int(self.id),
            "cash": float(self.cash),
            "skill": float(self.skill),
            "employed": bool(self.is_employed),
            "wage": float(self.wage),
            "reservation_wage": float(self.reservation_wage),
            "subsistence_failed": bool(self.subsistence_failed),
            "contract_remaining": int(self.contract_remaining),
            "inventory": float(self.inventory)
        }
