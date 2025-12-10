import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Slider } from "@/components/ui/slider";

interface ControlPanelProps {
    isManual: boolean;
    manualAction: any;
    agentAction: any;
    onToggleManual: () => void;
    onActionChange: (key: string, val: number) => void;
}

export function ControlPanel({ isManual, manualAction, agentAction, onToggleManual, onActionChange }: ControlPanelProps) {
    const [models, setModels] = useState<string[]>([]);
    const [selectedModel, setSelectedModel] = useState<string>("economy_ppo_final");
    const [loadingModel, setLoadingModel] = useState(false);

    useEffect(() => {
        // 1. Fetch available models
        fetch('http://localhost:8000/models')
            .then(res => res.json())
            .then(data => setModels(data.models))
            .catch(err => console.error("Failed to fetch models", err));

        // 2. Load saved model preference
        const savedModel = localStorage.getItem('sim_selected_model');
        if (savedModel) {
            setSelectedModel(savedModel);
            // Sync backend
            loadModel(savedModel);
        }
    }, []);

    const loadModel = (modelName: string) => {
        setLoadingModel(true);
        fetch('http://localhost:8000/load_model', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ model_name: modelName })
        }).then(res => res.json())
            .then(data => {
                console.log(data.message);
                setLoadingModel(false);
            })
            .catch(() => setLoadingModel(false));
    };

    const handleModelChange = (value: string) => {
        setSelectedModel(value);
        localStorage.setItem('sim_selected_model', value);
        loadModel(value);
    };

    return (
        <Card className="bg-slate-900 border-slate-800">
            <CardHeader className="flex flex-row items-center justify-between">
                <CardTitle className="text-slate-200">Policy Controls</CardTitle>
                <Button
                    variant={isManual ? "default" : "outline"}
                    size="sm"
                    onClick={onToggleManual}
                    className={isManual ? "bg-blue-600" : "border-slate-600 text-slate-400"}
                >
                    {isManual ? "Manual Mode" : "AI Agent Mode"}
                </Button>
            </CardHeader>
            <CardContent className="space-y-6">
                {/* Model Selector (Only visible in AI Mode) */}
                {!isManual && (
                    <div className="mb-6">
                        <label className="text-sm font-medium text-slate-300 mb-2 block">Active AI Model</label>
                        <select
                            className="w-full bg-slate-950 border border-slate-700 text-slate-200 rounded p-2 text-sm"
                            value={selectedModel}
                            onChange={(e) => handleModelChange(e.target.value)}
                            disabled={loadingModel}
                        >
                            {models.map(m => (
                                <option key={m} value={m}>{m}</option>
                            ))}
                        </select>
                        {loadingModel && <p className="text-xs text-yellow-400 mt-1">Loading model...</p>}
                    </div>
                )}

                <ControlSlider
                    label="Income Tax"
                    value={isManual ? manualAction.income_tax : agentAction.income_tax}
                    onChange={(v: number) => onActionChange('income_tax', v)}
                    disabled={!isManual}
                    color="bg-blue-500"
                />
                <ControlSlider
                    label="Corporate Tax"
                    value={isManual ? manualAction.corp_tax : agentAction.corp_tax}
                    onChange={(v: number) => onActionChange('corp_tax', v)}
                    disabled={!isManual}
                    color="bg-purple-500"
                />
                <ControlSlider
                    label="UBI (Subsidy)"
                    value={isManual ? manualAction.ubi : agentAction.ubi}
                    max={1000}
                    onChange={(v: number) => onActionChange('ubi', v)}
                    disabled={!isManual}
                    color="bg-green-500"
                />

                <div className="mt-8 p-4 bg-slate-950 rounded-lg border border-slate-800">
                    <h4 className="text-sm font-semibold text-slate-400 mb-2">
                        {isManual ? "Manual Override Active" : "Agent Logic Active"}
                    </h4>
                    <p className="text-xs text-slate-500">
                        {isManual
                            ? "You are in full control. The AI is disabled."
                            : `The RL Agent (${selectedModel}) is adjusting these values in real-time.`}
                    </p>
                </div>
            </CardContent>
        </Card>
    );
}

function ControlSlider({ label, value, max = 1.0, color, onChange, disabled }: any) {
    return (
        <div>
            <div className="flex justify-between mb-2">
                <span className="text-sm font-medium text-slate-300">{label}</span>
                <span className="text-sm text-slate-400">{max === 1.0 ? (value * 100).toFixed(1) + '%' : value.toFixed(0)}</span>
            </div>
            <Slider
                value={[value]}
                max={max}
                step={max === 1.0 ? 0.01 : 1}
                className={color}
                disabled={disabled}
                onValueChange={(vals) => onChange && onChange(vals[0])}
            />
        </div>
    );
}
