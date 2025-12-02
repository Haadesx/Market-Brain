import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
    title: "MarketBrain",
    description: "AI-Powered Financial Research Platform",
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en" className="dark">
            <body className={inter.className}>
                <div className="min-h-screen bg-background text-foreground">
                    <nav className="border-b border-border p-4">
                        <div className="container mx-auto flex justify-between items-center">
                            <h1 className="text-xl font-bold">MarketBrain 🧠</h1>
                            <div className="space-x-4">
                                <a href="/" className="hover:text-primary">Dashboard</a>
                                <a href="/backtest" className="hover:text-primary">Backtest</a>
                            </div>
                        </div>
                    </nav>
                    <main className="container mx-auto p-4">
                        {children}
                    </main>
                </div>
            </body>
        </html>
    );
}
