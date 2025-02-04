import logging
import os
from datetime import datetime


# TODO: NEED TO CREATE INFORMATIVE LOGGING
# docstring style = NumPy/SciPy
class SingletonLogger:
    """
    SingletonLogger is a singleton class that sets up a logger with file and console handlers.
    It ensures that only one instance of the logger is created and used throughout the application.

    Attributes
    ----------
    _instance : SingletonLogger
        The single instance of the SingletonLogger class.
    _logger : logging.Logger
        The logger instance.
    _setup_done : bool
        Flag to ensure the setup is done only once.
    log_directory : str
        The directory where log files are stored.
    all_file_handler : logging.FileHandler
        File handler for logging all levels.
    error_file_handler : logging.FileHandler
        File handler for logging error levels.
    console_handler : logging.StreamHandler
        Console handler for logging.

    Methods
    -------
    __new__(cls)
        Creates a new instance of SingletonLogger if one does not already exist.
    _setup()
        Sets up the logger with file and console handlers.
    _check_and_create_log_directory()
        Checks and creates the log directory if it does not exist.
    _set_logger_level()
        Sets the logger level to DEBUG.
    _create_file_handlers()
        Creates file handlers for logging all levels and error levels.
    _create_console_handler()
        Creates a console handler for logging.
    _set_formatters()
        Sets the formatters for the file and console handlers.
    _add_handlers()
        Adds the file and console handlers to the logger.
    get_class_logger()
        Returns a LoggerAdapter with the class name added to the log messages
    get_logger()
        Returns the logger instance.

    Usage example
    -------------
    >>> logger = SingletonLogger().get_logger()
    >>> logger.info('This is an info message')

    >>> class_name_logger = SingletonLogger().get_class_logger(self.__class__.__name__)
    >>> class_name_logger.info('This is an info message from class_name')
    """

    _instance = None

    def __new__(cls, _id: str = 'NoneDefault'):
        """
        Creates a new instance of SingletonLogger if one does not already exist.

        Returns
        -------
        SingletonLogger
            The single instance of the SingletonLogger class.
        """
        if cls._instance is None:
            cls._instance = super(SingletonLogger, cls).__new__(cls)
            cls._id = _id
            cls._instance._setup()
        return cls._instance

    def _setup(self) -> None:
        """
        Sets up the logger with file and console handlers, and ensures the setup is done only once.
        """
        self._logger = logging.getLogger(__name__)
        self._setup_done = False
        if not self._setup_done:
            self._check_and_create_log_directory()
            self._set_logger_level()
            self._create_file_handlers()
            self._create_console_handler()
            self._set_formatters()
            self._add_handlers()
            self._setup_done = True

    def _check_and_create_log_directory(self) -> None:
        """
        Checks if the 'data' folder exists. If not, raises an error.
        Checks if the 'logs' folder exists within 'data'. If not, creates it.
        """
        if not os.path.exists('data'):
            raise FileNotFoundError(
                "The 'data' folder does not exist. Please create it before running the application.")

        self.log_directory = os.path.join('data', 'logs')
        if not os.path.exists(self.log_directory):
            os.makedirs(self.log_directory)

    def _set_logger_level(self) -> None:
        """
        Sets the logger level to DEBUG.
        """
        self._logger.setLevel(logging.DEBUG)

    def _create_file_handlers(self) -> None:
        """
        Creates file handlers for logging all levels and error levels.
        """
        now = datetime.now()
        date_time_string = now.strftime("%Y-%m-%d")
        self.all_file_handler = logging.FileHandler(
            os.path.join(self.log_directory, f'crawler-{date_time_string}.txt'), 'w', 'utf-8')
        self.all_file_handler.setLevel(logging.DEBUG)

        self.error_file_handler = logging.FileHandler(
            os.path.join(self.log_directory, f'crawler-errors-{date_time_string}.txt'), 'w', 'utf-8')
        self.error_file_handler.setLevel(logging.ERROR)

    def _create_console_handler(self) -> None:
        """
        Creates a console handler for logging.
        """
        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(logging.DEBUG)

    def _set_formatters(self) -> None:
        """
        Sets the formatters for the file and console handlers.
        """
        formatter = logging.Formatter(f'ID : {self._id} - %(asctime)s - %(levelname)s - %(message)s')
        self.all_file_handler.setFormatter(formatter)
        self.error_file_handler.setFormatter(formatter)
        self.console_handler.setFormatter(formatter)

    def _add_handlers(self) -> None:
        """
        Adds the file and console handlers to the logger.
        """
        self._logger.addHandler(self.all_file_handler)
        self._logger.addHandler(self.error_file_handler)
        self._logger.addHandler(self.console_handler)

    def get_class_logger(self, class_name: str) -> logging.LoggerAdapter:
        """
        Returns a LoggerAdapter with the class name added to the log messages.

        :param class_name: Name of the class to be added to log messages
        :return: LoggerAdapter instance with class name context

        Usage example:
        >>>    logger = SingletonLogger().get_class_logger(self.__class__.__name__)
        >>>    logger.info('This is an info message from class_name')
        """
        return logging.LoggerAdapter(self._logger, {'class_name': class_name})

    def get_logger(self) -> logging.Logger:
        """
        Returns the logger instance.

        This logger does not include class-specific context and is useful for general logging.

        :return: Logger instance

        Usage example:
        >>>    logger = SingletonLogger().get_logger()
        >>>    logger.info('This is a general info message')
        """
        return self._logger
