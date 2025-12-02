# MarketBrain Architecture

## 1. System Overview

MarketBrain is a modular, service-oriented research platform designed to ingest financial data, extract features, train forecasting models, and provide insights via a Web UI and API.

### Core Capabilities
- **Multi-source Ingestion**: OHLCV, Fundamentals, News, Social Sentiment.
- **Advanced NLP**: Sentiment analysis using FinBERT.
- **ML Forecasting**: Multiple horizons (Next-day, Short-term) using Trees and Deep Learning.
- **Interactive UI**: Visualization, Backtesting, and Data Exploration.

## 2. Technology Stack

- **Backend**: Python 3.10+, FastAPI
- **Frontend**: TypeScript, Next.js, React, Tailwind CSS
- **Database**: PostgreSQL 14+ with TimescaleDB (Time-series), Redis (Cache/Broker)
- **Object Storage**: MinIO (S3 compatible) for model artifacts and raw logs
- **ML/Data**: PyTorch, Scikit-Learn, XGBoost, Hugging Face Transformers, Pandas/Polars
- **Orchestration**: Prefect (or Airflow)
- **Tracking**: MLflow
- **Containerization**: Docker, Docker Compose

## 3. Component Architecture

```mermaid
graph TD
    subgraph "External Data Sources"
        API_Market[Market Data APIs\n(AlphaVantage, Polygon, etc.)]
        API_News[News APIs\n(NewsAPI, RSS)]
        API_Social[Social APIs\n(Reddit, Twitter)]
    end

    subgraph "Ingestion Layer"
        Ingest_Market[Market Data Service]
        Ingest_News[News Ingestion Service]
        Ingest_Social[Social Sentiment Service]
    end

    subgraph "Storage Layer"
        DB_TS[(TimescaleDB\nMarket Data & Features)]
        DB_Rel[(PostgreSQL\nMetadata & Fundamentals)]
        Cache[(Redis\nReal-time & Queue)]
        S3[(MinIO S3\nArtifacts & Raw Data)]
    end

    subgraph "Processing & ML"
        NLP[NLP Service\n(FinBERT)]
        Feat_Eng[Feature Engine]
        Trainer[Model Trainer]
        Evaluator[Model Evaluator]
        MLflow[MLflow Server]
    end

    subgraph "Serving Layer"
        API_Gateway[FastAPI Gateway]
        WS_Server[WebSocket Server]
    end

    subgraph "User Interface"
        Web_UI[Next.js Web App]
    end

    API_Market --> Ingest_Market
    API_News --> Ingest_News
    API_Social --> Ingest_Social

    Ingest_Market --> DB_TS
    Ingest_News --> NLP
    Ingest_Social --> NLP

    NLP --> DB_TS
    NLP --> DB_Rel

    Feat_Eng --> DB_TS
    Feat_Eng --> Cache

    DB_TS --> Trainer
    Trainer --> MLflow
    Trainer --> S3
    Trainer --> Evaluator
    Evaluator --> DB_Rel

    API_Gateway --> DB_TS
    API_Gateway --> DB_Rel
    API_Gateway --> Cache
    API_Gateway --> MLflow

    WS_Server --> Cache

    Web_UI --> API_Gateway
    Web_UI --> WS_Server
```

## 4. Data Flow

1.  **Ingestion**: Scheduled jobs (Prefect) trigger Ingestion Services to fetch data from external APIs.
2.  **Raw Storage**: Raw JSON responses are optionally archived in S3; parsed structured data goes to Postgres/TimescaleDB.
3.  **NLP Pipeline**: Text data (News, Social) flows through the NLP Service for entity recognition (Ticker) and sentiment scoring (FinBERT). Scores are stored as time-series data.
4.  **Feature Engineering**: A Feature Engine computes derived metrics (Technical Indicators, Moving Averages, Aggregated Sentiment) and stores them in a "Feature Store" (TimescaleDB hypertable).
5.  **Training**: The Model Trainer queries the Feature Store, trains models (XGBoost/LSTM), logs metrics to MLflow, and saves artifacts to S3.
6.  **Serving**: The FastAPI Gateway serves historical data, features, and model predictions (loaded from S3/MLflow). Real-time updates are pushed via WebSockets.

## 5. Database Schema (High-Level)

### `market_data` (TimescaleDB Hypertable)
- `time` (TIMESTAMPTZ, PK)
- `symbol` (TEXT, PK)
- `open`, `high`, `low`, `close` (DECIMAL)
- `volume` (BIGINT)
- `source` (TEXT)

### `news_articles`
- `id` (UUID, PK)
- `published_at` (TIMESTAMPTZ)
- `title` (TEXT)
- `url` (TEXT)
- `source` (TEXT)
- `sentiment_score` (FLOAT)
- `sentiment_label` (TEXT)

### `social_posts`
- `id` (TEXT, PK)
- `platform` (TEXT) -- Reddit, Twitter
- `created_at` (TIMESTAMPTZ)
- `content` (TEXT)
- `author` (TEXT)
- `sentiment_score` (FLOAT)

### `features` (TimescaleDB Hypertable)
- `time` (TIMESTAMPTZ, PK)
- `symbol` (TEXT, PK)
- `feature_name` (TEXT) -- e.g., 'rsi_14', 'sentiment_1h'
- `value` (FLOAT)

### `predictions` (TimescaleDB Hypertable)
- `time` (TIMESTAMPTZ, PK) -- Prediction Time
- `target_time` (TIMESTAMPTZ) -- Forecast Target Time
- `symbol` (TEXT, PK)
- `model_version` (TEXT)
- `horizon` (TEXT) -- e.g., '1d', '1h'
- `predicted_value` (FLOAT)
- `confidence` (FLOAT)

### `fundamentals`
- `symbol` (TEXT, PK)
- `report_date` (DATE, PK)
- `metric` (TEXT) -- e.g., 'PE', 'EPS'
- `value` (FLOAT)

## 6. Directory Structure

```
/
├── backend/
│   ├── app/
│   │   ├── api/            # FastAPI Routes
│   │   ├── core/           # Config, Logging
│   │   ├── db/             # Database connection & models
│   │   ├── services/       # Business Logic (Ingestion, NLP)
│   │   ├── ml/             # Training & Inference Logic
│   │   └── schemas/        # Pydantic Models
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── lib/
│   ├── Dockerfile
│   └── package.json
├── notebooks/              # Research & Experiments
├── docker-compose.yml
├── Makefile
└── README.md
```
