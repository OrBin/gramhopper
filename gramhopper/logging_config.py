import logging


def configure_logger():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(
        logging.Formatter(
            '%(asctime)s %(module)s.%(funcName)s %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
        )
    )

    root_logger.addHandler(console_handler)
