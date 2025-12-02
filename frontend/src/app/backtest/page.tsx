"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

export default function BacktestPage() {
    const [result, setResult] = useState<any>(null)
    const [loading, setLoading] = useState(false)

    const runBacktest = async () => {
        setLoading(true)
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1500))
        setResult({
            totalReturn: 15.4,
            sharpeRatio: 1.8,
            trades: 42,
            winRate: 65
        })
        setLoading(false)
    }

    return (
        <div className="space-y-6">
            <h1 className="text-3xl font-bold">Backtest Lab</h1>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card className="md:col-span-1">
                    <CardHeader>
                        <CardTitle>Configuration</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="space-y-2">
                            <label className="text-sm font-medium">Strategy</label>
                            <select className="w-full h-10 rounded-md border border-input bg-background px-3 py-2 text-sm">
                                <option>ML Prediction (Long/Short)</option>
                                <option>Sentiment Momentum</option>
                                <option>Mean Reversion</option>
                            </select>
                        </div>
                        <div className="space-y-2">
                            <label className="text-sm font-medium">Ticker</label>
                            <Input placeholder="AAPL" defaultValue="AAPL" />
                        </div>
                        <div className="space-y-2">
                            <label className="text-sm font-medium">Initial Capital</label>
                            <Input type="number" defaultValue="10000" />
                        </div>
                        <Button className="w-full" onClick={runBacktest} disabled={loading}>
                            {loading ? "Running..." : "Run Backtest"}
                        </Button>
                    </CardContent>
                </Card>

                <Card className="md:col-span-2">
                    <CardHeader>
                        <CardTitle>Results</CardTitle>
                    </CardHeader>
                    <CardContent>
                        {result ? (
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                                <div className="p-4 bg-secondary rounded-lg text-center">
                                    <p className="text-sm text-muted-foreground">Total Return</p>
                                    <p className="text-2xl font-bold text-green-500">+{result.totalReturn}%</p>
                                </div>
                                <div className="p-4 bg-secondary rounded-lg text-center">
                                    <p className="text-sm text-muted-foreground">Sharpe Ratio</p>
                                    <p className="text-2xl font-bold">{result.sharpeRatio}</p>
                                </div>
                                <div className="p-4 bg-secondary rounded-lg text-center">
                                    <p className="text-sm text-muted-foreground">Trades</p>
                                    <p className="text-2xl font-bold">{result.trades}</p>
                                </div>
                                <div className="p-4 bg-secondary rounded-lg text-center">
                                    <p className="text-sm text-muted-foreground">Win Rate</p>
                                    <p className="text-2xl font-bold">{result.winRate}%</p>
                                </div>
                            </div>
                        ) : (
                            <div className="h-[300px] flex items-center justify-center text-muted-foreground border-2 border-dashed rounded-lg">
                                Run a backtest to see results
                            </div>
                        )}
                    </CardContent>
                </Card>
            </div>
        </div>
    )
}
