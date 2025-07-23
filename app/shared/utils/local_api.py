import httpx

BASE_URL = "http://localhost:8000"

async def call_api(endpoint: str, props: dict) -> dict:
    url = BASE_URL + endpoint
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=props)
        response.raise_for_status()
        return response.json()