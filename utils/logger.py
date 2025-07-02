import logging

def setup_logger(name: str, level=logging.INFO) -> logging.Logger:
    """
    建立一個只輸出到 console 的 logger。

    :param name: logger 名稱（一般使用模組名）
    :param level: logging 等級（預設 INFO）
    :return: logging.Logger 物件
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.hasHandlers():
        return logger
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger
