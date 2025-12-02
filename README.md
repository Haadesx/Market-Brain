# MarketBrain 🧠

**AI-Powered Financial Research Platform**

MarketBrain is a production-grade system designed to ingest financial data, extract features, train forecasting models, and provide actionable insights via a modern Web UI and API.

> [!WARNING]
> **Disclaimer**: This software is for educational and research purposes only. It is NOT financial advice. Trading stocks and crypto involves significant risk.

## 🏗 Architecture

MarketBrain follows a modular, service-oriented architecture containerized with Docker.

- **Frontend**: Next.js, React, Tailwind CSS, Recharts.
- **Backend**: FastAPI (Python), SQLAlchemy, Pydantic.
- **Data**: PostgreSQL (TimescaleDB), Redis.
- **ML**: PyTorch (LSTM), XGBoost, FinBERT (Sentiment), MLflow (Tracking).
- **Storage**: MinIO (S3-compatible).

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose
- Make (optional, for convenience commands)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/marketbrain.git
   cd marketbrain
   ```

2. **Configure Environment**
   Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your API keys (Alpha Vantage, NewsAPI, etc.).

3. **Start the Stack**
   ```bash
   make up
   # OR
   docker-compose up -d
   ```

4. **Access Services**
   - **Web UI**: [http://localhost:3000](http://localhost:3000)
   - **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
   - **MLflow**: [http://localhost:5000](http://localhost:5000)
   - **MinIO**: [http://localhost:9001](http://localhost:9001) (User/Pass: minioadmin)
   - **Adminer (DB)**: [http://localhost:8080](http://localhost:8080)

## ☁️ Deployment (Render)

1. **Push to GitHub**: Ensure this repository is pushed to your GitHub account.
2. **Create New Blueprint**:
   - Go to [Render Dashboard](https://dashboard.render.com/).
   - Click **New +** -> **Blueprint**.
   - Connect your repository.
   - Render will detect `render.yaml` and prompt you to apply it.
3. **Environment Variables**:
   - You will be prompted to enter values for `ALPHA_VANTAGE_API_KEY` and `NEWS_API_KEY`.
4. **Deploy**: Click **Apply** and wait for the services to build.

**Note**: The free tier of Render spins down services after inactivity. The first request might be slow.

## 🧪 Development

### Running Tests
```bash
make test
```

### Database Migrations
```bash
make migrate
```

### Project Structure
```
/
├── backend/            # FastAPI application & ML logic
│   ├── app/
│   │   ├── api/        # REST endpoints
│   │   ├── ml/         # Models & Training Pipeline
│   │   ├── services/   # Data Ingestion & Feature Engine
│   │   └── models/     # Database Schemas
├── frontend/           # Next.js Web Application
├── docker-compose.yml  # Infrastructure definition
└── Makefile            # Helper scripts
```

## 📊 Features

- **Multi-Source Ingestion**: Market data, News, Social Sentiment.
- **Advanced NLP**: FinBERT-based sentiment scoring.
- **ML Forecasting**: XGBoost and LSTM models for price direction.
- **Backtesting**: Simulate strategies on historical data.
- **Real-Time**: WebSocket streaming for live updates.

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

[MIT](https://choosealicense.com/licenses/mit/)
