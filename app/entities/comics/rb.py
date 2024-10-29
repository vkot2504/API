class RBComic:
    def __init__(self, id: int | None = None,
                 description: str | None = None,
                 rating: int | None = None,
                 user_id: int | None = None):
        self.id = id
        self.description = description
        self.rating = rating
        self.user_id = user_id

        
    def to_dict(self) -> dict:
        data = {'id': self.id, 'description': self.description, 'rating': self.rating, 'user_id': self.user_id}

        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data