from typing import Dict, Optional, Text, TypedDict

from fastapi.testclient import TestClient

from fastapi_chat.schemas.oauth import Token, User


def get_token(
    client: TestClient,
    *,
    username: Text,
    password: Text,
    reclaim: bool = False,
    cache: Optional[Dict[Text, Token]] = None
) -> Token:

    if cache is not None and username in cache and not reclaim:
        return cache[username]

    login_data = {"username": username, "password": password}
    response = client.post("/auth/login", data=login_data)
    response.raise_for_status()

    token = Token.model_validate(response.json())

    if cache is not None:
        cache[username] = token
    return token


async def auth_me(
    client: TestClient, login_data: "LoginData", *, cache_tokens: Dict[Text, Token]
) -> "User":
    user = User.model_validate(
        client.get(
            "/auth/me",
            headers=get_token(
                client=client, **login_data, cache=cache_tokens
            ).to_headers(),
        ).json()
    )
    assert user
    return user


class LoginData(TypedDict):
    username: Text
    password: Text
