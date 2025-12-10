"use client";

import { useEffect, useState, useRef } from 'react';
import { Sidebar } from "@/components/dashboard/Sidebar";
import { Header } from "@/components/dashboard/Header";
import { KpiGrid } from "@/components/dashboard/KpiGrid";
import { ControlPanel } from "@/components/dashboard/ControlPanel";
import { Charts } from "@/components/dashboard/Charts";
import { FirmsTable } from "@/components/dashboard/FirmsTable";
import { HouseholdsTable } from "@/components/dashboard/HouseholdsTable";

// Types for our data
interface SimulationData {
  step: number;
  gdp: number;
  real_gdp: number;
  unemployment: number;
  avg_price: number;
  avg_wage: number;
  inflation_rate: number;
  tax_revenue: number;
  govt_cash: number;
  subsistence_failures: number;
  gini: number;
  action: {
    income_tax: number;
    corp_tax: number;
    ubi: number;
  };
  firms: Array<{
    id: number;
    cash: number;
    inventory: number;
    price: number;
    wage_offer: number;
    employees_count: number;
    bankruptcies: number;
    last_profit: number;
    tier: number;
    max_employees: number;
  }>;
  households: Array<{
    id: number;
    cash: number;
    skill: number;
    employed: boolean;
    wage: number;
    reservation_wage: number;
    subsistence_failed: boolean;
    contract_remaining: number;
  }>;
}

export default function Dashboard() {
  const [data, setData] = useState<SimulationData | null>(null);
  const [history, setHistory] = useState<SimulationData[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [isRunning, setIsRunning] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);

  const [speed, setSpeed] = useState(1.0);
  const [isManual, setIsManual] = useState(false);
  const [manualAction, setManualAction] = useState({ income_tax: 0.2, corp_tax: 0.2, ubi: 0 });

  // Navigation State
  const [activeView, setActiveView] = useState('overview');

  // Load settings from localStorage on mount
  useEffect(() => {
    const savedSpeed = localStorage.getItem('sim_speed');
    if (savedSpeed) setSpeed(parseFloat(savedSpeed));

    const savedManual = localStorage.getItem('sim_is_manual');
    if (savedManual) setIsManual(savedManual === 'true');

    const savedAction = localStorage.getItem('sim_manual_action');
    if (savedAction) setManualAction(JSON.parse(savedAction));
  }, []);

  // Save settings when changed
  useEffect(() => {
    localStorage.setItem('sim_speed', speed.toString());
  }, [speed]);

  useEffect(() => {
    localStorage.setItem('sim_is_manual', isManual.toString());
  }, [isManual]);

  useEffect(() => {
    localStorage.setItem('sim_manual_action', JSON.stringify(manualAction));
  }, [manualAction]);

  // Connect to WebSocket
  useEffect(() => {
    const connect = () => {
      const ws = new WebSocket('ws://localhost:8000/ws');

      ws.onopen = () => {
        console.log('Connected to Simulation Server');
        setIsConnected(true);
      };

      ws.onmessage = (event) => {
        const newData: SimulationData = JSON.parse(event.data);
        setData(newData);
        setHistory(prev => {
          const newHistory = [...prev, newData];
          if (newHistory.length > 100) newHistory.shift(); // Keep last 100 steps
          return newHistory;
        });
        // Sync running state if needed, but usually we control it locally via commands
      };

      ws.onclose = () => {
        console.log('Disconnected');
        setIsConnected(false);
        setTimeout(connect, 2000);
      };

      wsRef.current = ws;
    };

    connect();

    return () => {
      wsRef.current?.close();
    };
  }, []);

  const sendCommand = (type: string, payload: any = {}) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ type, ...payload }));
      if (type === 'START') setIsRunning(true);
      if (type === 'STOP') setIsRunning(false);
      if (type === 'RESET') {
        setIsRunning(false);
        setHistory([]);
      }
    }
  };

  const handleSpeedChange = (val: number[]) => {
    setSpeed(val[0]);
    sendCommand('SET_SPEED', { value: val[0] });
  };

  const toggleManual = () => {
    const newVal = !isManual;
    setIsManual(newVal);
    sendCommand('SET_MANUAL', { value: newVal });
    if (newVal) sendCommand('UPDATE_ACTION', manualAction);
  };

  const handleActionChange = (key: string, val: number) => {
    const newAction = { ...manualAction, [key]: val };
    setManualAction(newAction);
    sendCommand('UPDATE_ACTION', newAction);
  };

  if (!data) {
    return (
      <div className="flex h-screen items-center justify-center bg-slate-950 text-white">
        <div className="text-center animate-pulse">
          <h1 className="text-4xl font-bold text-blue-500 mb-4">EcoSim AI</h1>
          <p className="text-slate-400">Connecting to Neural Core...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-slate-950 text-slate-100 font-sans">
      {/* Sidebar */}
      <Sidebar activeView={activeView} onViewChange={setActiveView} />

      {/* Main Content */}
      <div className="flex-1 ml-64 flex flex-col">
        <Header
          step={data.step}
          isConnected={isConnected}
          speed={speed}
          isRunning={isRunning}
          onSpeedChange={handleSpeedChange}
          onCommand={sendCommand}
        />

        <main className="flex-1 p-8 overflow-y-auto">
          {/* KPI Grid is always visible at top? Or only on Overview? Let's keep it on Overview for now, or make it smaller. 
              Actually, let's keep it on Overview to avoid clutter on data tables. */}

          {activeView === 'overview' && (
            <div className="space-y-8 animate-in fade-in duration-500">
              <KpiGrid data={data} history={history} />

              <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div className="lg:col-span-1">
                  <ControlPanel
                    isManual={isManual}
                    manualAction={manualAction}
                    agentAction={data.action}
                    onToggleManual={toggleManual}
                    onActionChange={handleActionChange}
                  />
                </div>
                <div className="lg:col-span-2">
                  <Charts history={history} />
                </div>
              </div>
            </div>
          )}

          {activeView === 'firms' && (
            <div className="animate-in fade-in duration-500">
              <div className="mb-6">
                <h2 className="text-2xl font-bold text-slate-200">Firms Market Data</h2>
                <p className="text-slate-400">Real-time analysis of production, inventory, and labor demand.</p>
              </div>
              <FirmsTable firms={data.firms} />
            </div>
          )}

          {activeView === 'households' && (
            <div className="animate-in fade-in duration-500">
              <div className="mb-6">
                <h2 className="text-2xl font-bold text-slate-200">Households Demographics</h2>
                <p className="text-slate-400">Population wealth distribution, employment status, and skill levels.</p>
              </div>
              <HouseholdsTable households={data.households} />
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
