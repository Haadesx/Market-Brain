"use client"

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

interface PriceChartProps {
    data: any[];
}

export function PriceChart({ data }: PriceChartProps) {
    return (
        <Card className="w-full h-[400px]">
            <CardHeader>
                <CardTitle>Price History</CardTitle>
            </CardHeader>
            <CardContent className="h-[300px]">
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={data}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                        <XAxis
                            dataKey="time"
                            tickFormatter={(str) => new Date(str).toLocaleDateString()}
                            stroke="#888"
                        />
                        <YAxis domain={['auto', 'auto']} stroke="#888" />
                        <Tooltip
                            contentStyle={{ backgroundColor: '#1f2937', border: 'none' }}
                            labelStyle={{ color: '#9ca3af' }}
                        />
                        <Line
                            type="monotone"
                            dataKey="close"
                            stroke="#3b82f6"
                            strokeWidth={2}
                            dot={false}
                        />
                    </LineChart>
                </ResponsiveContainer>
            </CardContent>
        </Card>
    )
}
