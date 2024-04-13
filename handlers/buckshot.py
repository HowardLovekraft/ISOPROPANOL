from icecream import ic
from aiogram import Router, F
from aiogram.types import Message, BotCommand, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import keyboards.keyboards as kbs
import misc.game_generators as gen
from misc.game_generators import PlayerStats, PlayerData, RoundParams

router = Router()

class GameStates(StatesGroup):
    game_started = State()
    round_started = State()


async def show_table(host: PlayerStats, guest: PlayerStats) -> str:
    previews = []
    for player in (host, guest):
        previews.append(f"ИНВЕНТАРЬ {player.name} :\n{await gen.print_health(player.health)}\n")
    invs = []
    for items_list in host.inv, guest.inv:
        inventory = [item for item in items_list]
        if len(inventory) < 8:
            inventory.extend(["." for _ in range(8-len(inventory))])
        invs.append(" ".join(inventory) + "\n")
    ic(previews, invs)
    return previews[0] + invs[0] + previews[1] + invs[1]


@router.message(Command("buckshot"))
async def create_game(message: Message, state: FSMContext) -> None:
    msg = message.text.split(" ")
    data = await state.get_data()
    data["host"] = PlayerData(name="@" + str(message.from_user.username), id=message.from_user.id)
    data["guest_name"] = msg[1]
    await state.update_data(data=data)
    await message.reply(text=f"{data['guest_name']}, you're invited to Roulette game",
                        reply_markup=await kbs.create_game_ikb())


@router.message(GameStates.round_started)
async def play_round(message: Message, state: FSMContext) -> None:
    # table = await show_table()
    pass


@router.callback_query(F.data == "joined_in")
async def join_in(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    guest = callback.from_user.username # cuz username w/o "@" literal
    if "@" + guest == data["guest_name"]:
        # give callback
        await callback.answer(text=f"{guest} joined in")
        await state.set_state(GameStates.game_started)
        await callback.message.delete()
        await state.set_state(GameStates.round_started)
        # save guest info in MemoryStorage
        data["guest"] = PlayerData(id=callback.from_user.id, name=data["guest_name"])
        # generate round
        round_params = await gen.generate_round(data["host"].name, data["guest"].name)
        data["round_params"] = round_params
        await callback.message.answer(text="Okay, LeT'S stARt!")
        data["host_profile"], data["guest_profile"] = await gen.generate_players_profiles(data["host"],
                                                                                          data["guest"],
                                                                                          round_params)
        await callback.message.answer(text=await show_table(data["host_profile"], data["guest_profile"]))
        await state.clear()
    else:
        await callback.answer(text="You're not invited!")


        # print(f"{callback.from_user.username} tried to join in") FOR DEBUG
        # print(f"{guest} {data['guest']} needed to be") FOR DEBUG

