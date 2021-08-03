import sys
import requests
from database import DatabaseManager
from persistence_layer import BookmarkDatabase
from datetime import datetime
from abc import ABC, abstractclassmethod

db = DatabaseManager("bookmarks.db")
persistence = BookmarkDatabase()

# 비지니스 로직 계층
# 부분적으로 영속 계층과 표현 로직을 분리하기 때문에 느슨한 결합이다.
# Command 디자인 페턴 활용
# execute - 인터페이스


class Command(ABC):
    @abstractclassmethod
    def execute(self, data):
        pass


class CreateBookmarksTableCommand(Command):
    def execute(self, data=None):
        db.create_table(
            "bookmarks",
            {
                "id": "integer primary key autoincrement",
                "title": "text not null",
                "url": "text not null",
                "notes": "text",
                "date_added": "text not null",
            },
        )


# 북마크에 대한 타임스탬프의 제어 반전
class AddBookmarkCommand(Command):
    def execute(self, data, timestamp=None):
        data["date_added"] = timestamp or datetime.utcnow().isoformat()
        persistence.create(data)
        return True, None


class ListBookmarksCommand(Command):
    def __init__(self, order_by="date_added"):
        self.order_by = order_by

    def execute(self, data=None):
        return True, persistence.list(order_by=self.order_by)


class DeleteBookmarkCommand(Command):
    def execute(self, data):
        persistence.delete(data)
        return "Bookmark deleted!!"


class EditBookmarkCommand(Command):
    def execute(self, data):
        persistence.edit(data["id"], data["update"])  # <6>
        return True, None


class ImportGitHubStarsCommand(Command):
    def _extract_bookmark_info(self, repo):
        return {
            "title": repo["name"],
            "url": repo["html_url"],
            "notes": repo["description"],
        }

    def execute(self, data):
        bookmarks_imported = 0

        github_username = data["github_username"]
        next_page_of_results = f"https://api.github.com/users/{github_username}/starred"

        while next_page_of_results:
            starts_resp = requests.get(
                next_page_of_results,
                headers={"Accept": "application/vnd.github.v3.star+json"},
            )
            next_page_of_results = starts_resp.links.get("next", {}).get("url")

            for repo_info in starts_resp.json():
                repo = repo_info["repo"]

                if data["preserve_timestamps"]:
                    timestamp = datetime.strptime(
                        repo_info["starred_at"], "%Y-%m-%dT%H:%M:%SZ"
                    )
                else:
                    timestamp = None

                bookmarks_imported += 1
                AddBookmarkCommand().execute(
                    self._extract_bookmark_info(repo), timestamp=timestamp
                )

        return f"Imported {bookmarks_imported} bookmarks from starred repos!"


class QuitCommand(Command):
    def execute(self, data=None):
        sys.exit()