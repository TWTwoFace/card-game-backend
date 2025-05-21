from fastapi import APIRouter

from src.api.users import router as users_router
from src.api.register import router as reg_router
from src.api.login import router as log_router
from src.api.clans import router as clans_router
from src.api.statistics import router as stats_router
from src.api.cards import router as cards_router
from src.api.clan_actions import router as clan_act_router
from src.api.shops import router as shops_router
from src.api.matchmaking import router as matchmaking_router
from src.api.match_statistics import router as matches_router


__all__ = [
    'main_router'
]


main_router = APIRouter()

main_router.include_router(users_router)
main_router.include_router(stats_router)
main_router.include_router(cards_router)
main_router.include_router(matches_router)
main_router.include_router(reg_router)
main_router.include_router(log_router)
main_router.include_router(clans_router)
main_router.include_router(clan_act_router)
main_router.include_router(shops_router)
main_router.include_router(matchmaking_router)
