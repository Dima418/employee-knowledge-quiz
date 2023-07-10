from httpx import AsyncClient


async def test_home(client: AsyncClient) -> None:
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}
