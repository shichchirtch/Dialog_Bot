from aiogram.types import BotCommand


async def set_main_menu(bot):
    main_menu_commands = [
        BotCommand(command='/basic_menu',
                   description='Загрузить анкету'),

        BotCommand(command='/help',
                   description='О работе бота')

    ]
    await bot.set_my_commands(main_menu_commands)
