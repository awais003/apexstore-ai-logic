from app.domain.ports.webhook_port import WebhookPort
import httpx
from app.core.exceptions import InfrastractureError


class HttpWebhookAdapter(WebhookPort):

    async def send(self, url: str, payload):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url=url, json=payload)
                response.raise_for_status()
        except httpx.TimeoutException as e:
            raise InfrastractureError(message=f"Webhook timeout: {str(e)}")
        except httpx.RequestError as e:
            raise InfrastractureError(message=f"Webhook connection error: {str(e)}")
        except httpx.HTTPStatusError as e:
            raise InfrastractureError(
                message=f"Webhook returned had status: {e.response.status_code}"
            )
        except Exception as e:
            raise InfrastractureError(message=f"Unexpected webhook error: {str(e)}")
