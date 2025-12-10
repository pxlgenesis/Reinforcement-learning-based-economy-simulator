import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

interface FirmsTableProps {
    firms: any[];
}

export function FirmsTable({ firms }: FirmsTableProps) {
    // Calculate summary stats
    const total = firms.length;
    const avgCash = firms.reduce((acc, f) => acc + f.cash, 0) / total;
    const avgWage = firms.reduce((acc, f) => acc + f.wage_offer, 0) / total;
    const avgPrice = firms.reduce((acc, f) => acc + f.price, 0) / total;
    const avgProfit = firms.reduce((acc, f) => acc + f.last_profit, 0) / total;
    const totalEmployees = firms.reduce((acc, f) => acc + f.employees_count, 0);
    const totalCapacity = firms.reduce((acc, f) => acc + f.max_employees, 0);

    return (
        <div className="space-y-4">
            <div className="grid grid-cols-4 gap-4">
                <Card className="bg-slate-900 border-slate-800 p-4">
                    <div className="text-sm text-slate-400">Avg Firm Cash</div>
                    <div className="text-2xl font-bold text-green-400">${avgCash.toFixed(0)}</div>
                </Card>
                <Card className="bg-slate-900 border-slate-800 p-4">
                    <div className="text-sm text-slate-400">Avg Wage Offer</div>
                    <div className="text-2xl font-bold text-yellow-400">${avgWage.toFixed(0)}</div>
                </Card>
                <Card className="bg-slate-900 border-slate-800 p-4">
                    <div className="text-sm text-slate-400">Avg Price</div>
                    <div className="text-2xl font-bold text-blue-400">${avgPrice.toFixed(2)}</div>
                </Card>
            </div>

            <Card className="bg-slate-900 border-slate-800">
                <CardHeader>
                    <CardTitle className="text-slate-200">Firms Status</CardTitle>
                </CardHeader>
                <CardContent className="max-h-[500px] overflow-y-auto">
                    <Table>
                        <TableHeader>
                            <TableRow className="border-slate-800 hover:bg-slate-900">
                                <TableHead className="text-slate-400">ID</TableHead>
                                <TableHead className="text-slate-400">Tier</TableHead>
                                <TableHead className="text-slate-400">Cash</TableHead>
                                <TableHead className="text-slate-400">Employees</TableHead>
                                <TableHead className="text-slate-400">Wage Offer</TableHead>
                                <TableHead className="text-slate-400">Price</TableHead>
                                <TableHead className="text-slate-400">Inventory</TableHead>
                                <TableHead className="text-slate-400">Profit (Last)</TableHead>
                                <TableHead className="text-slate-400">Bankruptcies</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {firms.map((f) => (
                                <TableRow key={f.id} className="border-slate-800 hover:bg-slate-800">
                                    <TableCell className="font-medium text-slate-200">{f.id}</TableCell>
                                    <TableCell className="text-blue-400 font-bold">
                                        T{f.tier}
                                    </TableCell>
                                    <TableCell className={f.cash < 0 ? "text-red-400" : "text-green-400"}>
                                        ${f.cash.toFixed(0)}
                                    </TableCell>
                                    <TableCell className="text-slate-300">
                                        {f.employees_count} / <span className="text-slate-500">{f.max_employees}</span>
                                    </TableCell>
                                    <TableCell className="text-slate-300">${f.wage_offer.toFixed(2)}</TableCell>
                                    <TableCell className="text-slate-300">${f.price.toFixed(2)}</TableCell>
                                    <TableCell className="text-slate-300">{f.inventory.toFixed(0)}</TableCell>
                                    <TableCell className={f.last_profit > 0 ? "text-green-400" : "text-red-400"}>
                                        ${f.last_profit.toFixed(0)}
                                    </TableCell>
                                    <TableCell className="text-slate-300">{f.bankruptcies}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>
        </div>
    );
}
