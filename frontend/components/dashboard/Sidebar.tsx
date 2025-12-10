import React from 'react';
import { LayoutDashboard, Building2, Users, Settings, BookOpen, Activity } from 'lucide-react';
import { Button } from "@/components/ui/button";

interface SidebarProps {
    activeView: string;
    onViewChange: (view: string) => void;
}

export function Sidebar({ activeView, onViewChange }: SidebarProps) {
    const navItems = [
        { id: 'overview', label: 'Overview', icon: LayoutDashboard },
        { id: 'firms', label: 'Firms Market', icon: Building2 },
        { id: 'households', label: 'Households', icon: Users },
        // { id: 'settings', label: 'Settings', icon: Settings },
        // { id: 'docs', label: 'Documentation', icon: BookOpen },
    ];

    return (
        <div className="h-screen w-64 bg-slate-950 border-r border-slate-800 flex flex-col fixed left-0 top-0">
            {/* Logo Area */}
            <div className="p-6 border-b border-slate-800">
                <div className="flex items-center gap-2 text-blue-500">
                    <Activity className="h-6 w-6" />
                    <span className="text-xl font-bold tracking-tight">EcoSim AI</span>
                </div>
                <p className="text-xs text-slate-500 mt-1">Reinforcement Learning Lab</p>
            </div>

            {/* Navigation */}
            <nav className="flex-1 p-4 space-y-2">
                {navItems.map((item) => (
                    <Button
                        key={item.id}
                        variant={activeView === item.id ? "secondary" : "ghost"}
                        className={`w-full justify-start gap-3 ${activeView === item.id
                                ? "bg-slate-800 text-blue-400 hover:bg-slate-800"
                                : "text-slate-400 hover:text-slate-100 hover:bg-slate-900"
                            }`}
                        onClick={() => onViewChange(item.id)}
                    >
                        <item.icon className="h-4 w-4" />
                        {item.label}
                    </Button>
                ))}
            </nav>

            {/* Footer / Status */}
            <div className="p-4 border-t border-slate-800">
                <div className="bg-slate-900 rounded-lg p-3">
                    <p className="text-xs text-slate-500 font-medium mb-1">System Status</p>
                    <div className="flex items-center gap-2">
                        <div className="h-2 w-2 rounded-full bg-green-500 animate-pulse" />
                        <span className="text-xs text-slate-300">Operational</span>
                    </div>
                </div>
            </div>
        </div>
    );
}
