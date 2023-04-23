import logging
from multiprocessing import Pool
from random import randint

from app.parser.loader import NewsViewer
from app.parser.news_list import get_news_links
from app.db.db import new_session
from app.db.models import Cookies

logging.basicConfig(level=logging.INFO)


def get_news() -> list[str]:
    return get_news_links()

def create_parser(_link, prof_id):
    viewer = NewsViewer(_link, prof_id)
    viewer.load()


def get_profiles_from_db(news):
    with new_session() as session:
        profiles = session.query(Cookies).all()
        if len(profiles) >= 5:
            active_profiles = profiles[:5]
            profiles = profiles[5::]
        else:
            active_profiles = profiles
        pool = Pool(5)
        # with Pool(5) as p:
        for prof in active_profiles:
            link = randint(0, len(news) - 1)
            res = pool.apply_async(create_parser, args=(news[link], prof.id))
            print(res)
        pool.close()
        pool.join()


def main() -> None:
    news = get_news()
    get_profiles_from_db(news)


if __name__ == "__main__":
    main()
