import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { DollarSign, Users, TrendingUp, Activity, Info } from 'lucide-react';

interface KpiGridProps {
    data: any;
    history: any[];
}

export function KpiGrid({ data, history }: KpiGridProps) {
    // Helper to get history array for a key
    const getHistory = (key: string) => history.map((h: any) => h[key] || 0);

    // Calculate Employment Stats
    const totalHouseholds = data.households ? data.households.length : 100;
    const employedCount = data.households ? data.households.filter((h: any) => h.employed).length : 0;
    const unemployedCount = totalHouseholds - employedCount;

    return (
        <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-8">
            <KpiCard
                title="Real GDP"
                value={`$${data.real_gdp.toLocaleString(undefined, { maximumFractionDigits: 0 })}`}
                icon={<DollarSign className="h-4 w-4 text-green-400" />}
                trend="Inflation Adjusted Production"
                color="text-green-400"
                history={getHistory('real_gdp')}
                description="Total value of goods produced, adjusted for inflation. The true health of the economy."
            />
            <KpiCard
                title="Nominal GDP"
                value={`$${data.gdp.toLocaleString(undefined, { maximumFractionDigits: 0 })}`}
                icon={<DollarSign className="h-4 w-4 text-slate-400" />}
                trend="Current Prices"
                color="text-slate-400"
                history={getHistory('gdp')}
                description="Total value of goods sold at current market prices. Can be inflated by price hikes."
            />
            <KpiCard
                title="Govt Cash"
                value={`$${data.govt_cash.toLocaleString(undefined, { maximumFractionDigits: 0 })}`}
                icon={<DollarSign className="h-4 w-4 text-blue-400" />}
                trend={data.govt_cash < 0 ? "Deficit" : "Surplus"}
                color={data.govt_cash < 0 ? "text-red-400" : "text-blue-400"}
                history={getHistory('govt_cash')}
                description="The government's treasury balance. Used for UBI and bailouts."
            />
            <KpiCard
                title="Unemployment"
                value={`${(data.unemployment * 100).toFixed(1)}%`}
                subValue={`${unemployedCount} Unemployed / ${employedCount} Employed`}
                icon={<Users className="h-4 w-4 text-red-400" />}
                trend={data.unemployment > 0.1 ? "Critical Level" : "Stable Level"}
                color={data.unemployment > 0.1 ? "text-red-500" : "text-green-400"}
                history={getHistory('unemployment')}
                description="Percentage of workforce without jobs. High unemployment leads to poverty."
                inverseTrend={true}
            />
            <KpiCard
                title="Avg Price"
                value={`$${data.avg_price.toFixed(2)}`}
                icon={<TrendingUp className="h-4 w-4 text-yellow-400" />}
                trend="Price Level"
                color="text-yellow-400"
                history={getHistory('avg_price')}
                description="Average price of goods in the market. Tracks inflation."
                inverseTrend={true}
            />
        </div>
    );
}

function KpiCard({ title, value, subValue, icon, trend, color, history, description, inverseTrend = false }: any) {
    // Calculate Trend %
    let trendPercent = 0;
    let trendDirection = 'neutral'; // 'up', 'down', 'neutral'

    if (history && history.length >= 2) {
        const current = history[history.length - 1];
        const previous = history[history.length - 2];

        if (previous !== 0) {
            trendPercent = ((current - previous) / previous) * 100;
        }

        if (trendPercent > 0.01) trendDirection = 'up';
        else if (trendPercent < -0.01) trendDirection = 'down';
    }

    // Determine Trend Color
    let trendColor = 'text-slate-400';
    if (trendDirection === 'up') trendColor = inverseTrend ? 'text-red-400' : 'text-green-400';
    if (trendDirection === 'down') trendColor = inverseTrend ? 'text-green-400' : 'text-red-400';

    return (
        <Card className="bg-slate-900 border-slate-800 relative group overflow-hidden">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-slate-400 flex items-center gap-2">
                    {title}
                    <div className="group-hover:opacity-100 opacity-0 transition-opacity absolute right-2 top-2 bg-slate-800 p-2 rounded text-xs text-slate-300 w-48 z-10 shadow-lg pointer-events-none">
                        {description}
                    </div>
                    <Info className="h-3 w-3 text-slate-600 cursor-help" />
                </CardTitle>
                {icon}
            </CardHeader>
            <CardContent>
                <div className="flex items-baseline gap-2">
                    <div className={`text-2xl font-bold ${color}`}>{value}</div>
                    {trendDirection !== 'neutral' && (
                        <div className={`text-xs font-medium flex items-center ${trendColor}`}>
                            {trendDirection === 'up' ? '↑' : '↓'} {Math.abs(trendPercent).toFixed(1)}%
                        </div>
                    )}
                </div>
                {subValue && <div className="text-xs text-slate-400 mt-1">{subValue}</div>}

                <div className="h-16 mt-4 w-full opacity-75">
                    <Sparkline data={history} color={color.replace('text-', '')} />
                </div>

                <p className="text-xs text-slate-500 mt-2">{trend}</p>
            </CardContent>
        </Card>
    );
}

function Sparkline({ data, color }: { data: number[], color: string }) {
    if (!data || data.length < 2) return null;

    const min = Math.min(...data);
    const max = Math.max(...data);
    const range = max - min || 1;

    // SVG Dimensions (internal coordinate system)
    const width = 100;
    const height = 50;
    const padding = 5; // Padding to prevent clipping

    // Generate Points
    const points = data.map((val, i) => {
        const x = (i / (data.length - 1)) * width;
        // Invert Y because SVG 0 is top
        // Scale to height - 2*padding, shift down by padding
        const normalizedVal = (val - min) / range;
        const y = (height - padding) - (normalizedVal * (height - 2 * padding));
        return `${x},${y}`;
    }).join(' ');

    // Map Tailwind colors to Hex for SVG stroke
    const colorMap: Record<string, string> = {
        'green-400': '#4ade80',
        'slate-400': '#94a3b8',
        'blue-400': '#60a5fa',
        'red-400': '#f87171',
        'red-500': '#ef4444',
        'yellow-400': '#facc15',
        'slate-100': '#f1f5f9'
    };

    const strokeColor = colorMap[color] || '#cbd5e1';

    return (
        <svg viewBox={`0 0 ${width} ${height}`} className="w-full h-full overflow-visible" preserveAspectRatio="none">
            <polyline
                fill="none"
                stroke={strokeColor}
                strokeWidth="2"
                points={points}
                vectorEffect="non-scaling-stroke"
                strokeLinecap="round"
                strokeLinejoin="round"
            />
        </svg>
    );
}
