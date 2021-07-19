import sys
from database import DatabaseManager
from datetime import datetime

db = DatabaseManager('bookmarks.db')

# 비지니스 로직 계층 
# 부분적으로 영속 계층과 표현 로직을 분리하기 때문에 느슨한 결합이다.
# Command 디자인 페턴 활용
class CreateBookmarksTableCommand:
    def execute(self):
        db.create_table('bookmarks', {
            'id': 'integer primary key autoincrement',
            'title': 'text not null',
            'url': 'text not null',
            'notes': 'text',
            'date_added': 'text not null',
        })
        
class AddBookmarkCommand:
    def execute(self, data):
        data['date_added'] = datetime.utcnow().isoformat()
        db.add('bookmarks', data)
        return 'Bookmark added!!'
    
class ListBookmarkCommand:
    def __init__(self, order_by='date_added'):
        self.order_by = order_by
        
    def execute(self):
        return db.select('bookmarks', order_by=self.order_by).fetchall()
    
class DeleteBookmarkCommand:
    def execute(self, data):
        db.delete('bookmarks', {'id': data})
        return 'Bookmark deleted!!'
    
class QuitCommand:
    def execute(self):
        sys.exit()