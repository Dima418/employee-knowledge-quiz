async def test_home(client) -> None:
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}
