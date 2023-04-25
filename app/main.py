import logging
from multiprocessing import Pool
from random import randint

from db.create_db import create_db
from db.db import new_session
from db.models import Profile
from parser.loader import NewsViewer
from parser.news_list import get_news_links

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
MAX_PROCESS = 5


def get_news() -> list[str]:
    return get_news_links()


def create_parser(_link: str, prof: int) -> None:
    viewer = NewsViewer(_link, prof)
    result = viewer.load()
    logger.info(result)


def get_profiles_from_db() -> list[int]:
    with new_session() as session:
        profiles = session.query(Profile).all()
        return [x.id for x in profiles]


def news_reader(profiles: list[int], news: list[str]) -> None:
    logger.info(f"Profiles quantities {len(profiles)}")
    while profiles:
        if len(profiles) >= MAX_PROCESS:
            active_profiles = profiles[:MAX_PROCESS]
            profiles = profiles[MAX_PROCESS::]
        else:
            active_profiles = profiles
            profiles = []
        pool = Pool(MAX_PROCESS)
        for prof in active_profiles:
            link = randint(0, len(news) - 1)
            pool.apply_async(create_parser, args=(news[link], prof))
        pool.close()
        pool.join()


def main() -> None:
    create_db()
    news = get_news()
    logger.info(f"\n New count = {len(news)}\n")
    profiles = get_profiles_from_db()
    news_reader(profiles, news)


if __name__ == "__main__":
    main()
