import sys
import requests
from database import DatabaseManager
from datetime import datetime

db = DatabaseManager('bookmarks.db')

# 비지니스 로직 계층 
# 부분적으로 영속 계층과 표현 로직을 분리하기 때문에 느슨한 결합이다.
# Command 디자인 페턴 활용
# execute - 인터페이스
class CreateBookmarksTableCommand:
    def execute(self):
        db.create_table('bookmarks', {
            'id': 'integer primary key autoincrement',
            'title': 'text not null',
            'url': 'text not null',
            'notes': 'text',
            'date_added': 'text not null',
        })

# 북마크에 대한 타임스탬프의 제어 반전        
class AddBookmarkCommand:
    def execute(self, data, timestamp=None):
        data['date_added'] = timestamp or datetime.utcnow().isoformat()
        db.add('bookmarks', data)
        return 'Bookmark added!!'
    
class ListBookmarksCommand:
    def __init__(self, order_by='date_added'):
        self.order_by = order_by

    def execute(self):
        return db.select('bookmarks', order_by=self.order_by).fetchall()
    
class DeleteBookmarkCommand:
    def execute(self, data):
        db.delete('bookmarks', {'id': data})
        return 'Bookmark deleted!!'

class ImportGitHubStarsCommand:
    def _extract_bookmark_info(self, repo):
        return {
            'title': repo['name'],
            'url': repo['html_url'],
            'notes': repo['description'],
        }
    
    def execute(self, data):
        bookmarks_imported = 0
        
        github_username = data['github_username']
        next_page_of_results = f'https://api.github.com/users/{github_username}/starred'
        
        while next_page_of_results:
            starts_resp = requests.get(
                next_page_of_results,
                headers={'Accept': 'application/vnd.github.v3.star+json'},
            )
            next_page_of_results = starts_resp.links.get('next', {}).get('url')
            
            for repo_info in starts_resp.json():
                repo = repo_info['repo']
                
                if data['preserve_timestamps']:
                    timestamp = datetime.strptime(
                        repo_info['starred_at'],
                        '%Y-%m-%dT%H:%M:%SZ'
                    )
                else:
                    timestamp = None
                
                bookmarks_imported += 1
                AddBookmarkCommand().execute(
                    self._extract_bookmark_info(repo),
                    timestamp=timestamp
                )
        
        return f'Imported {bookmarks_imported} bookmarks from starred repos!'

class QuitCommand:
    def execute(self):
        sys.exit()