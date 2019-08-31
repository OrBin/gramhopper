import operator
from boolean import boolean

OPERATOR_TO_FUNCTION = {
    boolean.AND: operator.and_,
    boolean.OR: operator.or_,
    boolean.NOT: operator.invert
}
