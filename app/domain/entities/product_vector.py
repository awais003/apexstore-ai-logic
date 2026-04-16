from app.domain.entities.entity import Entity
from typing import List, Dict


class ProductVector(Entity):

    def __init__(self, id: int, embeddings: List[float], metadata: Dict) -> None:
        self.id = id
        self.embeddings = embeddings
        self.metadata = metadata
