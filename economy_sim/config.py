# Simulation Constants
N_HOUSEHOLDS = 100
N_FIRMS = 10

# Economic Parameters
SUBSISTENCE_COST = 100.0  # Minimum cost to survive per month
AVG_PRODUCTIVITY = 10.0  # Average value produced by a worker per month (Reduced from 300 to prevent oversupply)
INITIAL_CASH_HOUSEHOLD = 500.0
INITIAL_CASH_FIRM = 100000.0 # Increased from 20k to 100k to survive initial wage bills

# Stability Constraints
WAGE_FLOOR = SUBSISTENCE_COST  # Workers won't accept less than survival cost
PRICE_STICKINESS = 0.05  # Max price change per step (+/- 5%)
HIRING_BUFFER_MONTHS = 3  # Firms need 3 months of wages in cash to hire
INVENTORY_DEPRECIATION = 0.10  # 10% of unsold goods rot per month

# RL Parameters
EPISODE_LENGTH = 360  # 30 Years (1 Step = 1 Month)
WARMUP_STEPS = 50  # Steps to run before AI takes control

# System
RANDOM_SEED = 42
