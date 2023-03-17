import os
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class PostrgresConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tg_bot: TgBot
    db: PostrgresConfig


def load_config():
    load_dotenv()

    return Config(
        tg_bot=TgBot(
            token=os.getenv("BOT_TOKEN")
        ),
        db=PostrgresConfig(
            host=os.getenv("DB_HOST"),
            password=os.getenv("DB_PASSWORD"),
            user=os.getenv("DB_USER"),
            database=os.getenv("DB_NAME"),
        )
    )


def get_postgres_uri():
    config = load_config()
    return f"postgresql://{config.db.user}:{config.db.password}@{config.db.host}/{config.db.database}"
