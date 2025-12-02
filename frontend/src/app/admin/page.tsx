"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"

export default function AdminPage() {

    return (
        <div className="space-y-6">
            <h1 className="text-3xl font-bold">Model Registry & Admin</h1>

            <div className="grid gap-6">
                {models.map((model) => (
                    <Card key={model.id}>
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-xl font-medium">
                                {model.type} <span className="text-muted-foreground text-sm">({model.horizon})</span>
                            </CardTitle>
                            <Badge variant={model.status === "Production" ? "default" : "secondary"}>
                                {model.status}
                            </Badge>
                        </CardHeader>
                        <CardContent>
                            <div className="flex justify-between items-center mt-4">
                                <div className="space-y-1">
                                    <p className="text-sm text-muted-foreground">Model ID</p>
                                    <p className="font-mono text-sm">{model.id}</p>
                                </div>
                                <div className="space-y-1">
                                    <p className="text-sm text-muted-foreground">RMSE</p>
                                    <p className="font-mono text-sm">{model.metrics.rmse}</p>
                                </div>
                                <div className="space-x-2">
                                    <Button variant="outline" size="sm" onClick={() => handleRetrain(model.id)}>
                                        Retrain
                                    </Button>
                                    {model.status !== "Production" && (
                                        <Button size="sm" onClick={() => handlePromote(model.id)}>
                                            Promote
                                        </Button>
                                    )}
                                </div>
                            </div>
                        </CardContent>
                    </Card>
                ))}
            </div>
        </div>
    )
}
