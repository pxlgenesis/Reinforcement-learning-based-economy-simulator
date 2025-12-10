import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface ChartsProps {
    history: any[];
}

export function Charts({ history }: ChartsProps) {
    return (
        <Card className="bg-slate-900 border-slate-800 lg:col-span-2 flex flex-col h-[500px]">
            <CardHeader>
                <CardTitle className="text-slate-200">Economic Indicators</CardTitle>
            </CardHeader>
            <CardContent className="flex-1 min-h-0">
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={history}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                        <XAxis dataKey="step" stroke="#475569" />
                        <YAxis yAxisId="left" stroke="#4ade80" tickFormatter={(value) => `$${value}`} />
                        <YAxis yAxisId="right" orientation="right" stroke="#f87171" />
                        <Tooltip
                            contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b' }}
                            itemStyle={{ color: '#e2e8f0' }}
                        />
                        <Line yAxisId="left" type="monotone" dataKey="real_gdp" stroke="#4ade80" strokeWidth={2} dot={false} name="Real GDP" />
                        <Line yAxisId="left" type="monotone" dataKey="gdp" stroke="#94a3b8" strokeWidth={1} strokeDasharray="5 5" dot={false} name="Nominal GDP" />

                        <Line yAxisId="right" type="monotone" dataKey="avg_price" stroke="#facc15" strokeWidth={2} dot={false} name="Avg Price" />
                        <Line yAxisId="right" type="monotone" dataKey="unemployment" stroke="#ef4444" strokeWidth={2} dot={false} name="Unemployment" />
                    </LineChart>
                </ResponsiveContainer>
            </CardContent>
        </Card>
    );
}
