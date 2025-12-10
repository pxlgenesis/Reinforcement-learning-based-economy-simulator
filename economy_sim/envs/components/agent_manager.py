import numpy as np
import random
from typing import List, Dict
from economy_sim.config import N_HOUSEHOLDS, N_FIRMS
from economy_sim.envs.components.household import Household
from economy_sim.envs.components.firm import Firm

class AgentManager:
    def __init__(self):
        self.households: List[Household] = [Household(i) for i in range(N_HOUSEHOLDS)]
        self.firms: List[Firm] = [Firm(i) for i in range(N_FIRMS)]
        
        # Global Market Stats (for Observation)
        self.total_tax_revenue = 0.0
        self.avg_price = 10.0
        self.avg_wage = 100.0
        self.unemployment_rate = 1.0
        self.gdp = 0.0
        self.gini = 0.0
        self.subsistence_failures = 0
        self.govt_cash = 100000.0 # Initial Reserves (Buffer)

    def step(self, tax_rates: Dict[str, float]):
        """
        Execute one month of economic activity.
        Order:
        1. Production (Firms produce goods based on labor).
        2. Labor Market (Hiring/Firing).
        3. Goods Market (Households buy goods).
        4. Taxes & Welfare (Govt collects/distributes).
        5. Agent Internal Updates (Consumption/Skill/Pricing).
        """
        income_tax = tax_rates.get("income_tax", 0.0)
        corp_tax = tax_rates.get("corp_tax", 0.0)
        ubi = tax_rates.get("ubi", 0.0)

        # --- 1. Production ---
        for firm in self.firms:
            # Calculate total skill of employees
            total_skill = sum([h.skill for h in self.households if h.employer_id == firm.id])
            firm.produce_goods(total_skill)
            
            # Pay Wages
            wage_bill = 0.0
            for h in self.households:
                if h.employer_id == firm.id:
                    # Firm pays full wage
                    wage_payment = firm.wage_offer 
                    firm.cash -= wage_payment
                    
                    # Deduct Income Tax at Source
                    tax = wage_payment * income_tax
                    net_wage = wage_payment - tax
                    self.total_tax_revenue += tax
                    
                    # Household receives Net Wage
                    h.cash += net_wage
                    h.wage = wage_payment # Track gross wage for stats
                    wage_bill += wage_payment
            
            # If firm can't pay wages, it's technically bankrupt/in debt
            # (Handled in firm.step() bankruptcy check)

        # --- 2. Labor Market ---
        # Firms try to hire
        # Only unemployed OR those with expired contracts look for work
        # Exception: Poaching (if wage offer is > 1.5x current wage)
        
        job_seekers = []
        for h in self.households:
            if not h.is_employed:
                job_seekers.append(h)
            elif h.contract_remaining <= 0:
                job_seekers.append(h) # Contract expired, free agent
            # Note: Poaching logic could go here, but let's keep it simple for Phase 1
        
        random.shuffle(job_seekers)
        
        # Firms post vacancies
        hiring_firms = [f for f in self.firms if f.cash > f.wage_offer * 3]
        firms_who_hired = set()
        
        # Track committed budget to prevent over-hiring
        # Map firm_id -> committed_cash
        committed_budget = {f.id: 0.0 for f in hiring_firms}
        
        # Shuffle hiring firms to prevent Firm 0 from grabbing all workers
        random.shuffle(hiring_firms)

        for h in job_seekers:
            # If already employed (contract expired), they have a current job
            # They will switch only if they find a better offer
            # If they don't find a better offer, they stay (renew contract)
            
            best_offer = None
            best_firm = None
            
            # If employed, their baseline is current wage
            current_wage = h.wage if h.is_employed else h.reservation_wage
            
            for f in hiring_firms:
                # Check if firm is at capacity
                if len(f.employees) >= f.max_employees:
                    continue

                # Check if firm still has budget for THIS hire
                cost_of_hire = f.wage_offer * 3 # Need 3 months buffer
                if (f.cash - committed_budget[f.id]) < cost_of_hire:
                    continue # Skip this firm, they are tapped out
                
                if f.wage_offer >= current_wage:
                    # Found a potential job
                    # In a simple model, take the first one that is better
                    # Or we could search for MAX. Let's take first better for now (Limited Search)
                    best_offer = f.wage_offer
                    best_firm = f
                    break 
            
            if best_firm:
                # Switch / Hire
                if h.is_employed:
                    # Quit old job
                    old_employer = next((f for f in self.firms if f.id == h.employer_id), None)
                    if old_employer and h.id in old_employer.employees:
                        old_employer.employees.remove(h.id)
                
                h.is_employed = True
                h.employer_id = best_firm.id
                h.wage = best_offer
                h.contract_remaining = 6 # 6 Month Contract
                best_firm.employees.append(h.id)
                firms_who_hired.add(best_firm.id)
                committed_budget[best_firm.id] += (best_offer * 3)
            elif h.is_employed:
                # Stay with old employer, renew contract
                # CHECK CAPACITY: If old employer is now full (e.g. downgraded tier), fire them
                old_employer = next((f for f in self.firms if f.id == h.employer_id), None)
                if old_employer and len(old_employer.employees) >= old_employer.max_employees:
                    # Laid off due to downsizing
                    h.is_employed = False
                    h.employer_id = None
                    h.wage = 0.0
                    h.contract_remaining = 0
                    # CRITICAL FIX: Remove from firm's list!
                    if h.id in old_employer.employees:
                        old_employer.employees.remove(h.id)
                else:
                    h.contract_remaining = 6
        
        # Check for failed hires
        for f in hiring_firms:
            if f.id not in firms_who_hired:
                f.failed_to_hire = True

        # --- 3. Goods Market ---
        # Households go shopping
        total_sales = 0
        total_revenue = 0.0
        
        # Shuffle households to ensure fair access to cheap goods
        shoppers = self.households[:]
        random.shuffle(shoppers)
        
        for h in shoppers:
            # Determine budget (Subsistence + Discretionary)
            # Simple rule: Spend 50% of cash above subsistence, plus subsistence
            budget = min(h.cash, 100.0 + (h.cash - 100.0) * 0.5) 
            if budget <= 0: continue
            
            spent = 0.0
            
            # Limited Search: Consumer checks 3 random firms and picks the cheapest
            # This prevents "Winner Takes All" where the absolute cheapest firm sells out instantly
            available_firms = [f for f in self.firms if f.inventory > 0]
            if not available_firms: continue
            
            # Sample up to 3 firms
            search_size = min(len(available_firms), 3)
            considered_firms = random.sample(available_firms, search_size)
            
            # Sort by price (Rational choice within the sample)
            considered_firms.sort(key=lambda x: x.price)

            for f in considered_firms:
                if f.inventory <= 0: continue # Should be handled by sample but safe check
                
                # How much can they buy?
                max_units = f.inventory
                affordable_units = (budget - spent) / f.price
                units_to_buy = min(max_units, affordable_units)
                
                if units_to_buy > 0:
                    cost = units_to_buy * f.price
                    
                    # Transaction
                    h.cash -= cost
                    h.inventory += units_to_buy
                    f.cash += cost
                    f.inventory -= units_to_buy
                    f.last_sales += units_to_buy
                    f.total_sales_revenue += cost
                    
                    spent += cost
                    total_sales += units_to_buy
                    total_revenue += cost
                    
        # Distribute UBI (Subject to Budget)
        # Calculate total needed
        total_ubi_needed = ubi * len(self.households)
        
        # Check affordability
        payout_per_person = ubi
        if total_ubi_needed > self.govt_cash:
            # Austerity: Only pay what we have
            if len(self.households) > 0:
                payout_per_person = self.govt_cash / len(self.households)
            else:
                payout_per_person = 0
        
        # Pay UBI
        for h in self.households:
            h.cash += payout_per_person
            self.govt_cash -= payout_per_person
            
        # Ensure we don't go negative due to float errors
        self.govt_cash = max(0.0, self.govt_cash)

        # --- 5. Internal Updates ---
        # Calculate Inflation Rate (Current Avg Price vs Last Avg Price)
        current_avg_price = np.mean([f.price for f in self.firms])
        inflation_rate = (current_avg_price - self.avg_price) / self.avg_price if self.avg_price > 0 else 0.0
        
        for h in self.households:
            h.step(inflation_rate)
        
        for f in self.firms:
            # Handle Bankruptcy
            if f.cash < 0:
                for emp_id in f.employees:
                    emp = self.households[emp_id]
                    emp.is_employed = False
                    emp.employer_id = None
                    emp.wage = 0.0
                    emp.contract_remaining = 0 # Void contract
                
                # Restructure with Govt Bailout logic
                # Calculate needed bailout
                bailout_needed = max(20000.0, f.wage_offer * 10 * 6)
                
                # Can Govt afford it?
                bailout_amount = 0.0
                if self.govt_cash >= bailout_needed:
                    bailout_amount = bailout_needed
                    self.govt_cash -= bailout_needed
                else:
                    # Govt is broke: Emergency Fed Printing (Inflationary Bailout)
                    # We MUST give enough to survive, or they die instantly again.
                    # Grant 3 months of wages + small buffer
                    bailout_amount = max(20000.0, f.wage_offer * 3)
                    # Do not deduct from govt_cash (it goes negative/printed)
                
                f._restructure(bailout_amount)
            else:
                f.step()

        # --- Bailout / Startup Logic ---
        active_firms = [f for f in self.firms if f.cash > 0]
        if len(active_firms) < 2:
            for f in self.firms:
                if f.cash <= 0:
                    # Revival Grant
                    grant = 20000.0
                    if self.govt_cash >= grant:
                        self.govt_cash -= grant
                    # Else: Free grant (Emergency)
                    
                    f._restructure(grant)
                    if len([x for x in self.firms if x.cash > 0]) >= 2:
                        break

        # --- Stats Update ---
        self.unemployment_rate = len([h for h in self.households if not h.is_employed]) / N_HOUSEHOLDS
        self.avg_price = np.mean([f.price for f in self.firms])
        self.avg_wage = np.mean([f.wage_offer for f in self.firms])
        
        # GDP = Total Consumption + Total Investment (Inventory Growth) + Govt Spending (UBI)
        # Simplified: GDP = Total Sales Revenue + Total Wages Paid
        # Actually, GDP (Income Approach) = Total Wages + Total Profits + Taxes
        total_wages = sum([h.wage for h in self.households if h.is_employed])
        total_profits = sum([f.last_profit for f in self.firms]) # last_profit is revenue before tax
        self.gdp = total_wages + total_profits
        
        # Gini Coefficient
        wealths = sorted([h.cash for h in self.households])
        self.gini = self._calculate_gini(wealths)
        
        # Subsistence Failures
        self.subsistence_failures = len([h for h in self.households if h.subsistence_failed])

    def _calculate_gini(self, wealths):
        """Calculate Gini coefficient of a list of wealths."""
        if not wealths: return 0.0
        total_wealth = sum(wealths)
        if total_wealth <= 0: return 0.0 # Avoid division by zero
        
        n = len(wealths)
        index = np.arange(1, n + 1)
        return ((2 * index - n - 1) * wealths).sum() / (n * total_wealth)

    def get_market_stats(self):
        return {
            "unemployment": self.unemployment_rate,
            "avg_price": self.avg_price,
            "avg_wage": self.avg_wage,
            "tax_revenue": self.total_tax_revenue,
            "gdp": self.gdp,
            "gini": self.gini,
            "subsistence_failures": self.subsistence_failures
        }
