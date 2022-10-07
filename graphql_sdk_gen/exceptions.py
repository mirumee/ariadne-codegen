class CodeGenException(Exception):
    """Generic graphql sdk gen exception."""


class ConfigFileNotFound(CodeGenException):
    """Config file not found."""


class MissingConfiguration(CodeGenException):
    """Configuration not present."""


class InvalidConfiguration(CodeGenException):
    """Configuration not valid."""


class InvalidGraphqlSyntax(CodeGenException):
    """Invalid graphql syntax."""


class NotSupported(CodeGenException):
    """Not supported."""


class ParsingError(CodeGenException):
    """Parsing error."""
