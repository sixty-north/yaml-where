class YAMLWhereException(Exception):
    pass


class MissingKeyError(YAMLWhereException, KeyError):
    pass


class UndefinedAccessError(YAMLWhereException):
    pass


class UnsupportedNodeTypeError(YAMLWhereException):
    pass