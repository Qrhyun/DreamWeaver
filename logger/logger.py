import logging
import logging.config
from datetime import datetime
from pathlib import Path

from util.util import read_json

'''
日志类
'''
def setup_logging(save_dir, log_config='logger/logger_config.json', default_level=logging.INFO):
    """
    Setup logging configuration
    """



    log_config = Path(log_config)
    if log_config.is_file():
        config = read_json(log_config)
        # modify logging paths based on run config
        for _, handler in config['handlers'].items():
            if 'filename' in handler:
                handler['filename'] = str(save_dir / handler['filename'])

        logging.config.dictConfig(config)
    else:
        print("Warning: logging configuration file is not found in {}.".format(log_config))
        logging.basicConfig(level=default_level)

def logFilePath(path):
    '''获取日志文件位置'''
    save_dir = Path(path)
    run_id = datetime.now().strftime('%d_%m_%Y')
    # 文件是否存在
    # exist_ok = run_id == ''
    # 创建log目录
    save_dir = save_dir / run_id

    save_dir.mkdir(parents=True,exist_ok=save_dir.exists())
    return  save_dir

