import logging
import os

from max_logger import MaxLogger
loger_token = os.environ.get('MAX_LOGGER_TOKEN')
recipient_ids = tuple(int(x.strip()) for x in os.environ["MAX_LOGGER_RECIPIENT_IDS"].split(","))

logger = MaxLogger(
    name='Offline conversions',
    project_file=__file__,
    token=loger_token,
    recipient_ids=recipient_ids,
    level=logging.DEBUG,
)
