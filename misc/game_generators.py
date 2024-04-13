# то, что по-хорошему надо вынести в отдельный файл
import random
import collections
from typing import NamedTuple
from misc.constants import constants

PlayerStats = collections.namedtuple("PlayerStats",
                                     ("id", "name","health", "inv"))
RoundParams = collections.namedtuple("Params", ("health", "queue",
                                                "player1_inv","player2_inv", "current_turn"))
PlayerData = collections.namedtuple("PlayerData", ("id", "name"))

async def generate_hp_amount() -> int:
    health_points = random.randint(2, 6)
    return health_points

async def print_health(hp_amount: int) -> str:
    hp_repr = "1" * hp_amount
    return hp_repr.ljust(8, "0")

async def generate_ammo_queue() -> tuple:
    total_amount = random.randint(2, 6)
    live_amount = random.randint(1, total_amount-1) # КОЛИЧЕСТВО БОЕВЫХ. -1 - ну чтобы blank >= 1
    blank_amount = total_amount - live_amount # КОЛИЧЕСТВО ХОЛОСТЫХ
    queue = tuple(constants["ammo_types"]["blank"] * blank_amount +
                  constants["ammo_types"]["live"] * live_amount)
    return queue

async def generate_inventories() -> tuple:
    items_amount = random.randint(0, 4)
    items1 = tuple(random.choice(constants["items"]) for _ in range(items_amount))
    items2 = tuple(random.choice(constants["items"]) for _ in range(items_amount))
    return items1, items2

async def generate_round(player1_name: str, player2_name: str, prev_turn: str = None) -> NamedTuple:
    health = await generate_hp_amount()
    queue = await generate_ammo_queue()
    player1_inv, player2_inv = await generate_inventories()
    if prev_turn is None:
        current_turn = random.choice((player1_name, player2_name))
    else:
        current_turn = player1_name if prev_turn == player2_name else player2_name

    return RoundParams(health, queue, player1_inv, player2_inv, current_turn)

async def generate_players_profiles(host: PlayerData,
                                    guest: PlayerData,
                                    round_params: RoundParams) -> tuple[PlayerStats, PlayerStats]:
    """
    :param host: id (Telegram's id, int, but as string) and username, str
    :param guest: id (Telegram's id, int, but as string) and username, str
    :param round_params: just parameters of round. That's simple.
    :return:
    """
    host_stats = PlayerStats(id=host.id, name=host.name,
                             health=round_params.health, inv=round_params.player1_inv)
    guest_stats = PlayerStats(id=guest.id, name=host.name,
                              health=round_params.health, inv=round_params.player2_inv)
    return host_stats, guest_stats
