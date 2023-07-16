class FTPError(Exception):
    pass


class BadLogFormatError(Exception):
    pass


class IntegrityError(Exception):
    pass


class InvalidChoiceError(Exception):
    pass


class CannotUpdateFieldError(Exception):
    pass


class UnrecognisedFieldError(Exception):
    pass


class InsufficientInformationError(Exception):
    pass


class Auth0Error(Exception):
    pass


class NoManualApprovalError(Exception):
    pass


class InvalidQueryError(Exception):
    pass


class EmptyGraphListError(Exception):
    pass


class InvalidBfsRunDetected(Exception):
    pass


class CyclicGraphError(Exception):
    pass


class InvalidParametersError(Exception):
    pass


class FlowCalculationError(Exception):
    pass


class NoPathsFoundError(Exception):
    pass


class BadOperatorError(Exception):
    pass
