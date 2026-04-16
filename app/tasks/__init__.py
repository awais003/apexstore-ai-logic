# app/tasks/__init__.py

# Import tasks from your sub-modules
from .tagging_task import tagging_products
from .indexing_task import indexing_products

# Define __all__ to control what is exported when someone
# uses 'from app.tasks import *'
__all__ = ["tagging_products", "indexing_products"]
