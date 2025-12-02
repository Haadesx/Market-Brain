"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Search } from "lucide-react"

export function TickerSearch() {
    const [symbol, setSymbol] = useState("")
    const router = useRouter()

    const handleSearch = (e: React.FormEvent) => {
        e.preventDefault()
        if (symbol) {
            router.push(`/ticker/${symbol.toUpperCase()}`)
        }
    }

    return (
        <form onSubmit={handleSearch} className="flex w-full max-w-sm items-center space-x-2">
            <Input
                type="text"
                placeholder="Search ticker (e.g. AAPL)"
                value={symbol}
                onChange={(e) => setSymbol(e.target.value)}
            />
            <Button type="submit" size="icon">
                <Search className="h-4 w-4" />
            </Button>
        </form>
    )
}
