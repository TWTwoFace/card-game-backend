from typing import Optional

from src.database import database as db
from src.models.matchmaking import MatchmakingRoom
from src.repositories.match_statistics import MatchStatisticsRepository


class MatchmakingRepository:
    @staticmethod
    async def get_all_rooms() -> Optional[list[MatchmakingRoom]]:
        try:
            record = await db.fetchmany(f"SELECT * FROM matchmakers_rooms")
            rooms = [MatchmakingRoom(**i) for i in record]

            return rooms
        except Exception as e:
            print(e)

    @staticmethod
    async def create_room(user_id: int) -> Optional[MatchmakingRoom]:
        try:
            await db.execute(f"INSERT INTO matchmakers_rooms (host_id) VALUES ('{user_id}')")

            record = await db.fetchone(f"SELECT * FROM matchmakers_rooms WHERE host_id='{user_id}'")
            room = MatchmakingRoom(**record)

            return room
        except Exception as e:
            print(e)

    @staticmethod
    async def join_room(user_id: int, room_id: int) -> bool:
        try:
            record = await db.fetchone(f"SELECT * FROM matchmakers_rooms WHERE id='{room_id}'")
            room = MatchmakingRoom(**record)

            if room.host_id == user_id:
                return False

            await db.execute(f"UPDATE matchmakers_rooms SET peer_id='{user_id}' WHERE id='{room_id}'")

            record = await db.fetchone(f"SELECT * FROM matchmakers_rooms WHERE id='{room_id}'")
            room = MatchmakingRoom(**record)

            await MatchStatisticsRepository.generate_match_stats(room)

            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    async def delete_room(user_id: int) -> bool:
        try:
            record = await db.fetchone(f"SELECT * FROM matchmakers_rooms WHERE host_id='{user_id}'")
            room = MatchmakingRoom(**record)

            await db.execute(f"DELETE FROM matchmakers_rooms WHERE id='{room.id}'")

            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    async def get_active_room(user_id: int) -> bool:
        try:
            record = await db.fetchone(f"SELECT COUNT(*) FROM matchmakers_rooms WHERE host_id='{user_id}'")

            return bool(record['count'])
        except Exception as e:
            print(e)
            return False
