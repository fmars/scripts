import uvicorn
from config import FEED_SERVICE_PORT, SERVICE_HOST
from fastapi import FastAPI
from post_service import Post, PostService
from utils import create_users, validate_users


class FeedService:
    def __init__(self, users: dict[str, set[str]]) -> None:
        self.users: dict[str, set[str]] = users

    def feed(self, uid: str, start_ts: float, end_ts: float) -> list[Post]:
        # Get the list of users that the user follows
        assert uid in self.users, f"User {uid} does not exist"
        friends = self.users.get(uid, set())
        posts = PostService.get_users_posts(friends + uid, start_ts, end_ts)
        posts.sort(key=lambda post: post.timestamp)
        return posts

    def query_post_service(self, uids: list[str], start_ts: float, end_ts: float) -> list[Post]:
        

def feed_service_handler(feed_service: FeedService) -> FastAPI:
    app = FastAPI()

    @app.get("/feed")
    def feed(user: str, start_ts: float, end_ts: float):
        print(f"Getting feed for user {user} between {start_ts} and {end_ts}")
        return feed_service.feed(user, start_ts, end_ts)

    return app


def create_feed_service() -> None:
    print(f"Starting feed service on {SERVICE_HOST}:{FEED_SERVICE_PORT}")
    users = create_users()
    validate_users(users)
    feed_service = FeedService(users)

    uvicorn.run(feed_service_handler(feed_service), host=SERVICE_HOST, port=FEED_SERVICE_PORT)


if __name__ == "__main__":
    create_feed_service()
