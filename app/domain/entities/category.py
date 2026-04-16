from app.domain.entities.entity import Entity


class Cateogry(Entity):

    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name
