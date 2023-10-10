import bot
import logging

logging.basicConfig(level=logging.INFO, filename="log.log", filemode="w")

while True:
    bot.start_bot()
    logging.info('Error occurred: restarting bot')
