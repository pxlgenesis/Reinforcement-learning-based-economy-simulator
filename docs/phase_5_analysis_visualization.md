# Phase 5: Analysis & Visualization - Detailed Specification

This document defines how we interpret the simulation results and the user interface for interacting with the economy.

## 1. Data Logging (The "Black Box" Recorder)
We need granular data to debug economic crashes.
*   **Format**: CSV or Parquet (for efficiency).
*   **Frequency**: Every step (Month).
*   **Data Points**:
    *   `Global`: Date, Tax Rates, GDP, Inflation, Gini.
    *   `Agent_Level` (Optional/Sampled): Wealth of Agent #1, #50, #99.

## 2. Metrics & Analytics
*   **Lorenz Curve**: Visual representation of inequality. We plot this at the end of every episode.
*   **Velocity of Money**: How fast is money changing hands? (GDP / Money Supply).
*   **Bankruptcy Rate**: % of firms that failed.
*   **Subsistence Failure Rate**: % of households that could not afford the minimum food cost (Poverty/Starvation metric).
*   **Employment Stats**:
    *   *Unemployment Rate*: % of workforce without a job.
    *   *Labor Utilization*: Total Hours Worked / Total Labor Capacity (Are we wasting human potential?).
*   **System Efficiency Metrics**:
    *   *Market Clearing Efficiency*: (Goods Sold / Goods Produced). Low score = Waste/Overproduction.
    *   *Capital Velocity*: (GDP / Money Supply). Low score = Hoarding/Stagnation.
    *   *Social Mobility Score*: Probability of a bottom-quintile agent reaching the top quintile over 10 years.

## 3. The Web Dashboard (The UI)
A React-based dashboard to visualize the logs.

### 3.1 Tech Stack
*   **Frontend**: Next.js (React) + TailwindCSS.
*   **UI Library**: Shadcn UI (for premium, accessible components).
*   **Charts**: `Recharts` or `React Force Graph`.
*   **Backend API**: Python `FastAPI`.
    *   *Communication*: **WebSockets** for real-time streaming (60fps) of agent positions and graph data. REST API for historical logs.

### 3.2 Views
*   **Overview Panel**:
    *   Big numbers: GDP, Population, Current Year.
    *   Sparklines for recent trends.
*   **Policy Control Panel** (Interactive Mode):
    *   Sliders for Tax Rates (if we want to play as the government manually).
*   **Agent Interaction View (The "Triangle" of Power)**:
    *   A dedicated section showing the 3-way flow: **Government <-> Firms <-> Households**.
    *   **Visuals**:
        *   *Govt -> Firms*: Arrows showing "Tax" (Red) vs "Subsidies" (Green).
        *   *Firms -> Households*: Arrows showing "Wages" (Gold).
        *   *Households -> Firms*: Arrows showing "Consumption" (Blue).
    *   **Live Stats per Sector**:
        *   *Government*: Current Approval Rating, Budget Balance.
        *   *Firms Sector*: Total Profit, Avg Price, **Total Inventory** (Recession Indicator).
        *   *Household Sector*: Avg Happiness, **Avg Skill Level**, **Avg Reservation Wage**.
    *   **Deep Dive Charts**:
        *   *Skill vs Wage*: Line chart comparing "Avg Skill" vs "Avg Real Wage".
        *   *The Wage Gap*: Line chart comparing "Avg Reservation Wage" vs "Avg Offered Wage". (Gap = Friction).
        *   *Wealth Distribution*: Histogram of agent wealth.

## 4. Post-Mortem Analysis
*   When the economy crashes, we need a "Crash Report".
*   *Cause Analysis*: Did tax hikes cause demand to drop? Did low interest rates cause hyperinflation?
*   We can use simple correlation analysis on the logs to generate these insights automatically.
