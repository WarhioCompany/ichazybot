import bot
while True:
    try:
        bot.start_bot()
    except Exception as e:
        print(f'Got ERROR: {e}. Restarting...')
        pass
