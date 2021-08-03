from abc import ABC, abstractclassmethod
from database import DatabaseManager

# 영속 계층 인터페이스를 정의하는 추상 기본 클래스
class PersistenceLayer(ABC):
    @abstractclassmethod
    def create(self, data):
        raise NotImplementedError("Persistence layers must implement a create method")

    @abstractclassmethod
    def list(self, data):
        raise NotImplementedError("Persistence layers must implement a list method")

    @abstractclassmethod
    def edit(self, data):
        raise NotImplementedError("Persistence layers must implement a update method")

    @abstractclassmethod
    def delete(self, data):
        raise NotImplementedError("Persistence layers must implement a delete method")


class BookmarkDatabase(PersistenceLayer):
    def __init__(self):
        self.table_name = "bookmarks"
        self.db = DatabaseManager("bookmarks.db")

        self.db.create_table(
            self.table_name,
            {
                "id": "integer primary key autoincrement",
                "title": "text not null",
                "url": "text not null",
                "notes": "text",
                "date_added": "text not null",
            },
        )

    def create(self, bookmark_data):
        self.db.add(self.table_name, bookmark_data)

    def list(self, order_by=None):
        return self.db.select(self.table_name, order_by=self.order_by).fetchall()

    def edit(self, bookmark_id, bookmark_data):
        self.db.update(self.table_name, {"id": bookmark_id}, bookmark_data)

    def delete(self, bookmark_id):
        self.db.add(self.table_name, {"id": bookmark_id})
