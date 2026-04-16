import logging

def setup_logging():
    # 1. Get the root logger
    root_logger = logging.getLogger()
    
    # 2. If Celery is already running, its handlers are likely already there.
    # We tell the root logger to stop double-processing if it's already handled.
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # 3. Create a clean, single handler
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s')
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # 4. Set the global level
    root_logger.setLevel(logging.INFO)

    # 5. CRITICAL: Silence library noise globally
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    
    # Optional: If specific app modules still double-log, silence them here
    # logging.getLogger("app.services").propagate = False