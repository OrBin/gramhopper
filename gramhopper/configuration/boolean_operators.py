import operator
from boolean import boolean

OPERATOR_TYPE_TO_FUNCTION = {
    boolean.AND: operator.and_,
    boolean.OR: operator.or_,
    boolean.NOT: operator.invert
}
