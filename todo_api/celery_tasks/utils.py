import logging

import httpx
from django.conf import settings

# Getting TEELGRAM Bot token from DJango settings
TELEGRAM_BOT_TOKEN = settings.TELEGRAM_SECRET_TOKENS[0]
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

logger = logging.getLogger(__name__)


async def send_telegram_message(chat_id: str, text: str):
    """
    Sends a message to Telegram.

    Parameters:
        Chat_id (str): Chat identifier in Telegram, where the message will be sent.
        Text (str): the text of the message that will be sent.

    Returns:
        Dict: API Telegram response in JSON format, if the message is sent successfully.

    Exceptions:
        Httpstatuserror: Error if the Telegram server returns the status of error code.
        Requesterror: Network error when trying to send a request.
        Exception: Any other error not provided above.
    """
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
    }

    # Sending Post-request to Telegram API
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(TELEGRAM_API_URL, json=payload)
            response.raise_for_status()

            logger.info(
                f"Уведомление успешно отправлено в Telegram (chat_id: {chat_id})"
            )
            return response.json()

        except httpx.HTTPStatusError as e:
            logger.error(
                f"Ошибка HTTP {e.response.status_code} при отправке в Telegram: {e.response.text}"
            )

        except httpx.RequestError as e:
            logger.error(f"Ошибка сети при отправке в Telegram: {str(e)}")

        except Exception as e:
            logger.error(f"Неизвестная ошибка при отправке в Telegram: {str(e)}")
