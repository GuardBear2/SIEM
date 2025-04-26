from typing import List

from pydantic import BaseModel
from guardbear.core.indexer.models.events import AgentMetadata, Header, TaskResult


class StatefulEvents(BaseModel):
    agent_metadata: AgentMetadata
    headers: List[Header]
    data: List[bytes]


class StatefulEventsResponse(BaseModel):
    results: List[TaskResult]
