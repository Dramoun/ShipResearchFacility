# custom_exceptions.py

class CustomError(Exception):
    """
    Base class for other exceptions.

    This is the base class for all custom exceptions in the project.
    """
    pass


class MissingGlobalVariableError(CustomError):
    """
    Raised when a required global variable is missing.

    Parameters
    ----------
    variable_name : str
        The name of the missing global variable.
    message : str, optional
        An optional custom error message (default is "Missing global variable").

    Attributes
    ----------
    variable_name : str
        The name of the missing global variable.
    message : str
        The error message.

    Examples
    --------
    >>> variable_name = "AZ_COPY_SECRET_KEY"
    >>> raise MissingGlobalVariableError(variable_name)
    MissingGlobalVariableError: Missing global variable: AZ_COPY_SECRET_KEY is not set.
    """
    def __init__(self, variable_name, message="Missing global variable"):
        """
        Initialize the MissingGlobalVariableError.

        Parameters
        ----------
        variable_name : str
            The name of the missing global variable.
        message : str, optional
            An optional custom error message (default is "Missing global variable").
        """
        self.variable_name = variable_name
        self.message = f"{message}: {variable_name} is not set."
        super().__init__(self.message)
