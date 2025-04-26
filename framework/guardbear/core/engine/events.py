from typing import AsyncGenerator

from httpx import RequestError
from guardbear.core.engine.base import APPLICATION_JSON, APPLICATION_NDJSON, BaseModule
from guardbear.core.engine.models.base import ErrorResponse
from guardbear.core.exception import GuardBearEngineError, GuardBearError


class EventsModule(BaseModule):
    """Events module to send stateless events to the Engine."""

    MODULE = 'events'

    async def send(self, event_stream: AsyncGenerator[bytes, None]) -> None:
        """Send events to the engine.

        Parameters
        ----------
        event_stream : AsyncGenerator[bytes, None]
            Events as a byte stream.

        Raises
        ------
        GuardBearError(2710)
            Invalid request error.
        """
        try:
            response = await self._client.post(
                url=f'{self.API_URL}/{self.MODULE}/stateless',
                content=event_stream,
                headers={
                    'Accept': APPLICATION_JSON,
                    'Content-Type': APPLICATION_NDJSON,
                },
            )

            if response.is_error:
                error = ErrorResponse(**response.json())
                raise GuardBearError(2710, extra_message=': '.join(error.error))

        except RequestError as exc:
            raise GuardBearEngineError(2803, extra_message=str(exc))
