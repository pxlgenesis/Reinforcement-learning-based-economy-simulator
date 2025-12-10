import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

interface HouseholdsTableProps {
    households: any[];
}

export function HouseholdsTable({ households }: HouseholdsTableProps) {
    // Calculate summary stats
    const total = households.length;
    const employed = households.filter(h => h.employed).length;
    const unemployed = total - employed;
    const avgSkill = households.reduce((acc, h) => acc + h.skill, 0) / total;
    const avgResWage = households.reduce((acc, h) => acc + h.reservation_wage, 0) / total;

    return (
        <div className="space-y-4">
            <div className="grid grid-cols-4 gap-4">
                <Card className="bg-slate-900 border-slate-800 p-4">
                    <div className="text-sm text-slate-400">Total Households</div>
                    <div className="text-2xl font-bold text-slate-200">{total}</div>
                </Card>
                <Card className="bg-slate-900 border-slate-800 p-4">
                    <div className="text-sm text-slate-400">Employed / Unemployed</div>
                    <div className="text-2xl font-bold text-slate-200">
                        <span className="text-green-400">{employed}</span> / <span className="text-red-400">{unemployed}</span>
                    </div>
                </Card>
                <Card className="bg-slate-900 border-slate-800 p-4">
                    <div className="text-sm text-slate-400">Avg Skill Level</div>
                    <div className="text-2xl font-bold text-blue-400">{avgSkill.toFixed(2)}</div>
                </Card>
                <Card className="bg-slate-900 border-slate-800 p-4">
                    <div className="text-sm text-slate-400">Avg Reservation Wage</div>
                    <div className="text-2xl font-bold text-yellow-400">${avgResWage.toFixed(2)}</div>
                </Card>
            </div>
            <div className="grid grid-cols-4 gap-4">
                <Card className="bg-slate-900 border-slate-800 p-4">
                    <div className="text-sm text-slate-400">Avg Job Security</div>
                    <div className="text-2xl font-bold text-blue-400">
                        {(households.filter(h => h.employed).reduce((acc, h) => acc + h.contract_remaining, 0) / (employed || 1)).toFixed(1)} mo
                    </div>
                </Card>
                <Card className="bg-slate-900 border-slate-800 p-4">
                    <div className="text-sm text-slate-400">Poverty Rate</div>
                    <div className="text-2xl font-bold text-red-400">
                        {((households.filter(h => h.subsistence_failed).length / total) * 100).toFixed(1)}%
                    </div>
                </Card>
                <Card className="bg-slate-900 border-slate-800 p-4">
                    <div className="text-sm text-slate-400">Avg Household Wealth</div>
                    <div className="text-2xl font-bold text-green-400">
                        ${(households.reduce((acc, h) => acc + h.cash, 0) / total).toFixed(0)}
                    </div>
                </Card>
                <Card className="bg-slate-900 border-slate-800 p-4">
                    <div className="text-sm text-slate-400">Avg Real Wage</div>
                    <div className="text-2xl font-bold text-yellow-400">
                        ${(households.filter(h => h.employed).reduce((acc, h) => acc + h.wage, 0) / (employed || 1)).toFixed(0)}
                    </div>
                </Card>
            </div>

            <Card className="bg-slate-900 border-slate-800">
                <CardHeader>
                    <CardTitle className="text-slate-200">Households Directory</CardTitle>
                </CardHeader>
                <CardContent className="max-h-[500px] overflow-y-auto">
                    <Table>
                        <TableHeader>
                            <TableRow className="border-slate-800 hover:bg-slate-900">
                                <TableHead className="text-slate-400">ID</TableHead>
                                <TableHead className="text-slate-400">Cash</TableHead>
                                <TableHead className="text-slate-400">Status</TableHead>
                                <TableHead className="text-slate-400">Contract</TableHead>
                                <TableHead className="text-slate-400">Skill</TableHead>
                                <TableHead className="text-slate-400">Wage</TableHead>
                                <TableHead className="text-slate-400">Res. Wage</TableHead>
                                <TableHead className="text-slate-400">Inventory</TableHead>
                                <TableHead className="text-slate-400">Subsistence</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {households.map((h) => (
                                <TableRow key={h.id} className="border-slate-800 hover:bg-slate-800">
                                    <TableCell className="font-medium text-slate-200">{h.id}</TableCell>
                                    <TableCell className={h.cash < 100 ? "text-red-400" : "text-green-400"}>
                                        ${h.cash.toFixed(0)}
                                    </TableCell>
                                    <TableCell className={h.employed ? "text-green-400" : "text-red-400"}>
                                        {h.employed ? "Employed" : "Unemployed"}
                                    </TableCell>
                                    <TableCell className="text-slate-300">
                                        {h.employed ? `${h.contract_remaining} mo` : "-"}
                                    </TableCell>
                                    <TableCell className="text-slate-300">{h.skill.toFixed(2)}</TableCell>
                                    <TableCell className="text-slate-300">${h.wage.toFixed(0)}</TableCell>
                                    <TableCell className="text-slate-300">${h.reservation_wage.toFixed(0)}</TableCell>
                                    <TableCell className={h.inventory < 1 ? "text-red-400 font-bold" : "text-slate-300"}>
                                        {h.inventory ? h.inventory.toFixed(1) : "0.0"}
                                    </TableCell>
                                    <TableCell className={h.subsistence_failed ? "text-red-500 font-bold" : "text-green-500"}>
                                        {h.subsistence_failed ? "FAILED" : "OK"}
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>
        </div>
    );
}
