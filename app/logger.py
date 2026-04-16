import logging

def setup_logger(name="app", level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.handlers:
        return logger  # Prevent duplicate logs

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
    )

    # Console output
    console = logging.StreamHandler()
    console.setFormatter(formatter)

    # File output
    file = logging.FileHandler("app.log")
    file.setFormatter(formatter)

    logger.addHandler(console)
    logger.addHandler(file)

    return logger
