import { TickerSearch } from "@/components/dashboard/TickerSearch"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export default function Home() {
    return (
        <div className="flex flex-col items-center justify-center min-h-[80vh] space-y-8">
            <div className="text-center space-y-4">
                <h1 className="text-4xl font-extrabold tracking-tight lg:text-5xl">
                    MarketBrain 🧠
                </h1>
                <p className="text-xl text-muted-foreground">
                    AI-Powered Financial Research & Forecasting
                </p>
            </div>

            <TickerSearch />

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-4xl mt-12">
                <Card>
                    <CardHeader>
                        <CardTitle>Deep Learning</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <p className="text-muted-foreground">
                            LSTM and Transformer models trained on price, volume, and sentiment.
                        </p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader>
                        <CardTitle>Sentiment Analysis</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <p className="text-muted-foreground">
                            Real-time NLP processing of news and social media using FinBERT.
                        </p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader>
                        <CardTitle>Backtesting</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <p className="text-muted-foreground">
                            Simulate strategies and evaluate performance metrics instantly.
                        </p>
                    </CardContent>
                </Card>
            </div>
        </div>
    )
}
