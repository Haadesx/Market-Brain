import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_health_check(ac: AsyncClient):
    response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "MarketBrain Backend"}

@pytest.mark.asyncio
async def test_root(ac: AsyncClient):
    response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to MarketBrain API"}

# Add more tests for market data, predictions, etc.
# Note: These would require a running DB or mocked DB session.
