from enum import Enum


class FilterOperator(str, Enum):
    LT = "<"
    GT = ">"
    EQ = "="
    NTQ = "!="
    LTE = "<="
    GTE = ">="
