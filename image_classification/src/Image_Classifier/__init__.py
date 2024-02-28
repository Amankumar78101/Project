import os
import sys
import logging
import datetime

logging_str = '[%(asctime)s %(levelname)s %(module)s] : %(message)s'

log_dir_name = 'log'
current_time = datetime.datetime.now()
log_dir = current_time.strftime('%Y_%m_%d')
LOG_FILE = current_time.strftime('%d_%H_%M_%S') + '.log'

log_filepath = os.path.join(log_dir_name, log_dir, LOG_FILE)

os.makedirs(os.path.join(log_dir_name, log_dir), exist_ok=True)

logging.basicConfig(level=logging.INFO,
                    format=logging_str,
                    handlers=[
                        logging.FileHandler(log_filepath),
                        logging.StreamHandler(sys.stdout)
                    ]
                    )
logger = logging.getLogger('Image_Classifier')
