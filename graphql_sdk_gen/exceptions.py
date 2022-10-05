class ConfigFileNotFound(Exception):
    """Config file not found."""


class MissingConfiguration(Exception):
    """Configuration not present."""


class InvalidConfiguration(Exception):
    """Configuration not valid."""


class InvalidGraphqlSyntax(Exception):
    """Invalid graphql syntax."""


class NotSupported(Exception):
    """Not supported."""


class ParsingError(Exception):
    """Parsing error."""
