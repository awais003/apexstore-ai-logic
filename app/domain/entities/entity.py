class Entity:
    def to_dict(self):
        result = {}

        for key, value in self.__dict__.items():
            if isinstance(value, Entity):
                result[key] = value.to_dict()

            elif isinstance(value, list):
                result[key] = [
                    item.to_dict() if isinstance(item, Entity) else item
                    for item in value
                ]

            else:
                result[key] = value

        return result
