from typing import Protocol


class WebhookPort(Protocol):

    async def send(self, url: str, payload: dict) -> None: ...
