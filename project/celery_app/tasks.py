import os

from celery_app.config_celery import app
from celery_app.functions import request_vk
from database.models.social_network import SocialNetwork
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

DATABASE_URL = (
    f"postgresql://"
    f"{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}"
    f"@localhost:5432/{os.getenv('POSTGRES_DB')}"
)


sync_engine = create_engine(DATABASE_URL)
sync_session = sessionmaker(sync_engine)


@app.task
def youtube_api():
    pass


@app.task
def vk_api():
    with sync_session() as session:
        social_networks = session.execute(select(
            SocialNetwork
        ).where(
                SocialNetwork.type == "V"
            )
        ).scalars().all()
        for sn in social_networks:
            try:
                followers, likes = request_vk(
                    username=sn.username_network
                )
                sn.followers_count = followers
                sn.likes_count = likes
                session.add(sn)
            except ValueError:
                continue
        session.commit()
