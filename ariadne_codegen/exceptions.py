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


class InvalidOperationForSchema(CodeGenException):
    """Invalid operation for the schema."""


class NotSupported(CodeGenException):
    """Not supported."""


class ParsingError(CodeGenException):
    """Parsing error."""


class IntrospectionError(CodeGenException):
    """Introspection error."""


class PluginImportError(CodeGenException):
    """Error occurred during the plugin lookup."""
