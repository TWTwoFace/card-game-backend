import random
from typing import Optional

from src.database import database as db
from src.models.matchmaking import MatchmakingRoom, MatchStatistics
from src.repositories.statistics import StatisticsRepository


class MatchStatisticsRepository:
    @staticmethod
    async def generate_match_stats(room: MatchmakingRoom):
        try:
            match_result = random.randint(0, 1)

            if match_result:
                await StatisticsRepository.add_win(room.peer_id)
                await StatisticsRepository.add_loose(room.host_id)
            else:
                await StatisticsRepository.add_win(room.host_id)
                await StatisticsRepository.add_loose(room.peer_id)

            await db.execute(f"INSERT INTO match_statistics (host_id, peer_id, room_id, result, duration) "
                             f"VALUES ('{room.host_id}', '{room.peer_id}', '{room.id}','{match_result}', '{random.randint(5, 20)}')")

            await db.execute(f"DELETE FROM matchmakers_rooms WHERE id='{room.id}'")
        except Exception as e:
            print(e)

    @staticmethod
    async def get_users_matches(user_id: int) -> Optional[list[MatchStatistics]]:
        try:
            record = await db.fetchmany(f"SELECT * FROM match_statistics WHERE peer_id='{user_id}' OR host_id='{user_id}'")
            matches = [MatchStatistics(**i) for i in record]

            return matches
        except Exception as e:
            print(e)
