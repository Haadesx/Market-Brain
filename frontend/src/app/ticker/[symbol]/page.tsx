"use client"

import { useEffect, useState } from "react"
import { useParams } from "next/navigation"
import { PriceChart } from "@/components/charts/PriceChart"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

// Mock data generator if backend is not reachable
const generateMockData = () => {
    const data = []
    let price = 150
    const now = new Date()
    for (let i = 30; i >= 0; i--) {
        const date = new Date(now)
        date.setDate(date.getDate() - i)
        price = price + (Math.random() - 0.5) * 5
        data.push({
            time: date.toISOString(),
            close: price,
            open: price - 1,
            high: price + 2,
            low: price - 2,
            volume: Math.floor(Math.random() * 1000000)
        })
    }
    return data
}

export default function TickerPage() {
    const params = useParams()
    const symbol = params.symbol as string
    const [data, setData] = useState<any[]>([])
    const [prediction, setPrediction] = useState<any>(null)

    useEffect(() => {
        // In a real app, fetch from API
        // fetch(\`http://localhost:8000/api/v1/market/history/\${symbol}...\`)

        setData(generateMockData())

        setPrediction({
            direction: Math.random() > 0.5 ? "UP" : "DOWN",
            confidence: 0.75,
            return: 0.012
        })
    }, [symbol])

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h1 className="text-3xl font-bold">{symbol}</h1>
                {prediction && (
                    <div className="flex items-center space-x-4">
                        <div className="text-right">
                            <p className="text-sm text-muted-foreground">Prediction (1d)</p>
                            <div className="flex items-center space-x-2">
                                <span className={`text-xl font-bold ${prediction.direction === 'UP' ? 'text-green-500' : 'text-red-500'}`}>
                                    {prediction.direction}
                                </span>
                                <span className="text-sm text-muted-foreground">
                                    {(prediction.confidence * 100).toFixed(0)}% Conf.
                                </span>
                            </div>
                        </div>
                    </div>
                )}
            </div>

            <PriceChart data={data} />

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Card>
                    <CardHeader>
                        <CardTitle>Sentiment Analysis</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-4">
                            <div className="flex justify-between items-center">
                                <span>News Sentiment</span>
                                <span className="text-green-500 font-bold">Positive</span>
                            </div>
                            <div className="flex justify-between items-center">
                                <span>Social Volume</span>
                                <span>High</span>
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader>
                        <CardTitle>Key Features</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-2">
                            <div className="flex justify-between">
                                <span className="text-muted-foreground">RSI (14)</span>
                                <span>58.4</span>
                            </div>
                            <div className="flex justify-between">
                                <span className="text-muted-foreground">MACD</span>
                                <span className="text-green-500">+1.24</span>
                            </div>
                            <div className="flex justify-between">
                                <span className="text-muted-foreground">Volatility (20d)</span>
                                <span>1.5%</span>
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    )
}
