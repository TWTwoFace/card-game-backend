from src.config.statistics import RATING_PER_WIN, RATING_PER_LOOSE
from src.models.statistics import UserStatisticsSchema
from src.database import database as db


class StatisticsRepository:
    @staticmethod
    async def get_statistics_by_user_id(user_id: int) -> UserStatisticsSchema:
        try:
            record = await db.fetchone(f"SELECT * FROM statistics WHERE user_id='{user_id}'")
            stats = UserStatisticsSchema(**record)
            return stats
        except Exception as e:
            print(e)

    @staticmethod
    async def add_win(user_id: int):
        try:
            await db.execute(f"UPDATE statistics "
                             f"SET"
                             f" matches_count=matches_count+1,"
                             f" win_count=win_count+1,"
                             f" current_rating=current_rating+{RATING_PER_WIN},"
                             f" max_rating=MAX(max_rating, current_rating)"
                             f"WHERE user_id = '{user_id}'")

            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    async def add_loose(user_id: int):
        try:
            await db.execute(f"UPDATE statistics "
                             f"SET"
                             f" matches_count=matches_count+1,"
                             f" current_rating=MAX(current_rating-{RATING_PER_LOOSE}),"
                             f"WHERE user_id = '{user_id}'")

            return True
        except Exception as e:
            print(e)
            return False
