import os
import logging

### @package log_setup
#
# Setup of logging
#

if not os.path.exists('data/'):
    os.mkdir('data/')

formatter = logging.Formatter("[{asctime}] [{levelname}] [{module}.{funcName}] {message}", style="{")

file_logger = logging.FileHandler('data/events.log')
file_logger.setFormatter(formatter)

console_logger = logging.StreamHandler()
console_logger.setFormatter(formatter)

logger = logging.getLogger('my-bot')
logger.setLevel(logging.INFO)
logger.addHandler(file_logger)
logger.addHandler(console_logger)
