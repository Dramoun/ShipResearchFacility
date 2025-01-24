import time
from typing import Callable, Optional


class Timer:
    """
    A context manager for timing code execution.

    Parameters
    ----------
    name : Optional[str]
        The name of the timer. If provided, it will be included in the output messages.
    output_func : Callable[[str], None]
        A function to handle the output messages. Defaults to the built-in print function.
    suppress_exceptions : bool
        Whether to suppress exceptions that occur within the context. Defaults to False.

    Methods
    -------
    __enter__() -> 'Timer'
        Starts the timer and returns the Timer instance.
    __exit__(exc_type: Optional[type], exc_val: Optional[Exception], exc_tb: Optional[object]) -> Optional[bool]
        Stops the timer, outputs the elapsed time, and handles exceptions.

    Examples
    --------
    >>> def custom_log(message: str) -> None:
    ...     print(f"LOG: {message}")
    ...
    >>> with Timer("Example Timer", output_func=custom_log, suppress_exceptions=True):
    ...     for i in range(1000000):
    ...         pass  # Simulating some work
    ...     raise ValueError("An example error")
    ...
    LOG: Timer 'Example Timer' started.
    LOG: Timer 'Example Timer' ended. Elapsed time: 0.1234 seconds.
    LOG: An exception of type ValueError occurred. Arguments: ('An example error',)
    """

    def __init__(self, name: Optional[str] = None, output_func: Callable[[str], None] = print,
                 suppress_exceptions: bool = False) -> None:
        """
        Initializes the Timer instance.

        Parameters
        ----------
        name : Optional[str]
            The name of the timer. If provided, it will be included in the output messages.
        output_func : Callable[[str], None]
            A function to handle the output messages. Defaults to the built-in print function.
        suppress_exceptions : bool
            Whether to suppress exceptions that occur within the context. Defaults to False.
        """
        self.name = name
        self.output_func = output_func
        self.suppress_exceptions = suppress_exceptions

    def __enter__(self) -> 'Timer':
        """
        Starts the timer and returns the Timer instance.

        Returns
        -------
        Timer
            The Timer instance.
        """
        self.start_time = time.time()
        self.output_func(self._start_message())
        return self

    def __exit__(self, exc_type: Optional[type],
                 exc_val: Optional[Exception],
                 exc_tb: Optional[object]) -> Optional[bool]:
        """
        Stops the timer, outputs the elapsed time, and handles exceptions.

        Parameters
        ----------
        exc_type : Optional[type]
            The exception type, if an exception was raised.
        exc_val : Optional[Exception]
            The exception value, if an exception was raised.
        exc_tb : Optional[object]
            The traceback object, if an exception was raised.

        Returns
        -------
        Optional[bool]
            Whether to suppress exceptions. If True, exceptions are suppressed.
        """
        self.end_time = time.time()
        self.elapsed_time = self.end_time - self.start_time

        if exc_type is not None:
            self.output_func(self._exception_message(exc_type, exc_val))

        self.output_func(self._end_message())

        return self.suppress_exceptions

    def _start_message(self) -> str:
        """
        Constructs the start message.

        Returns
        -------
        str
            The start message.
        """
        return f"Timer '{self.name}' started." if self.name else "Timer started."

    def _end_message(self) -> str:
        """
        Constructs the end message.

        Returns
        -------
        str
            The end message.
        """
        return f"Timer '{self.name}' ended. Elapsed time: {self.elapsed_time:.4f} seconds." \
            if self.name else f"Timer ended. Elapsed time: {self.elapsed_time:.4f} seconds."

    @staticmethod
    def _exception_message(exc_type: type, exc_val: Exception) -> str:
        """
        Constructs the exception message.

        Parameters
        ----------
        exc_type : type
            The exception type.
        exc_val : Exception
            The exception value.

        Returns
        -------
        str
            The exception message.
        """
        return f"An exception of type {exc_type.__name__} occurred. Arguments: {exc_val.args}"


if __name__ == '__main__':
    print('Running timer functionality on its own, it does nothing!')
