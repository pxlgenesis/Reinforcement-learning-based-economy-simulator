import React from 'react';
import { Button } from "@/components/ui/button";
import { Slider } from "@/components/ui/slider";
import { Play, Pause, RotateCcw, Clock } from 'lucide-react';

interface HeaderProps {
    step: number;
    isConnected: boolean;
    speed: number;
    isRunning: boolean;
    onSpeedChange: (val: number[]) => void;
    onCommand: (type: string) => void;
}

export function Header({ step, isConnected, speed, isRunning, onSpeedChange, onCommand }: HeaderProps) {
    return (
        <header className="h-16 border-b border-slate-800 bg-slate-950/50 backdrop-blur flex items-center justify-between px-6 sticky top-0 z-10">
            {/* Left: Breadcrumbs / Status */}
            <div className="flex items-center gap-4">
                <div className="flex items-center gap-2 text-slate-400 bg-slate-900 px-3 py-1 rounded-full border border-slate-800">
                    <Clock className="h-3 w-3" />
                    <span className="text-xs font-mono">Month {step} (Year {(step / 12).toFixed(1)})</span>
                </div>
                {!isConnected && (
                    <span className="text-xs text-red-500 bg-red-500/10 px-2 py-1 rounded">Offline</span>
                )}
            </div>

            {/* Right: Controls */}
            <div className="flex items-center gap-6">
                <div className="flex items-center gap-3 w-48">
                    <span className="text-xs text-slate-500 font-medium">SPEED</span>
                    <Slider
                        value={[speed]}
                        min={0.1}
                        max={10.0}
                        step={0.1}
                        onValueChange={onSpeedChange}
                        className="flex-1"
                    />
                    <span className="text-xs text-slate-400 w-8 text-right">{speed}x</span>
                </div>

                <div className="h-6 w-px bg-slate-800" />

                <div className="flex gap-2">
                    <Button
                        size="sm"
                        onClick={() => onCommand(isRunning ? 'STOP' : 'START')}
                        className={isRunning
                            ? "bg-yellow-500/10 text-yellow-500 hover:bg-yellow-500/20 border border-yellow-500/50"
                            : "bg-green-500/10 text-green-500 hover:bg-green-500/20 border border-green-500/50"
                        }
                    >
                        {isRunning ? <Pause className="mr-2 h-3 w-3" /> : <Play className="mr-2 h-3 w-3" />}
                        {isRunning ? "Pause" : "Resume"}
                    </Button>

                    <Button
                        size="sm"
                        variant="outline"
                        onClick={() => onCommand('RESET')}
                        className="border-slate-700 text-slate-400 hover:text-red-400 hover:border-red-400/50 hover:bg-red-400/10"
                    >
                        <RotateCcw className="mr-2 h-3 w-3" /> Reset
                    </Button>
                </div>
            </div>
        </header>
    );
}
