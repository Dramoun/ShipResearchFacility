import json
import os


class GeneralUtils:
    """
    General utility class for handling file operations such as reading, writing,
    appending, and clearing JSON files. This class is designed to be extensible for
    other general-purpose utilities.

    Available Methods
    -----------------
    - save_to_json(data, file_name): Saves data to a JSON file (overwrites existing content).
    - load_from_json(file_name): Loads and returns data from a JSON file.
    - append_to_json(new_data, file_name): Appends data to an existing JSON file.
    - clear_json_file(file_name): Clears the content of a JSON file (overwrites with an empty list).
    """

    @staticmethod
    def save_to_json(data: dict | list, file_name: str) -> None:
        """
        Saves data to a JSON file.

        Parameters
        ----------
        data : dict | list
            The data to be saved. Must be serializable to JSON.

        file_name : str
            The name of the JSON file where the data will be saved.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If the data is not serializable to JSON.
        IOError
            If there is an error writing to the file.

        Example
        -------
        >>> data = {"key": "value"}
        >>> GeneralUtils.save_to_json(data, "example.json")
        """
        try:
            with open(file_name, "w") as f:
                json.dump(data, f, indent=4)
        except TypeError as e:
            raise ValueError(f"Data is not serializable to JSON: {e}")
        except IOError as e:
            raise IOError(f"Error writing to file {file_name}: {e}")

    @staticmethod
    def load_from_json(file_name: str) -> dict | list[dict] | None:
        """
        Loads data from a JSON file.

        Parameters
        ----------
        file_name : str
            The name of the JSON file to be read.

        Returns
        -------
        dict | list[dict] | None
            The data loaded from the JSON file.
            None if error occured.

        Raises
        ------
        FileNotFoundError
            If the specified file does not exist.
        ValueError
            If the file contents are not valid JSON.
        IOError
            If there is an error reading the file.

        Example
        -------
        >>> data = GeneralUtils.load_from_json("example.json")
        >>> print(data)
        {'key': 'value'}
        """
        if not os.path.exists(file_name):
            raise FileNotFoundError(f"{file_name} does not exist.")

        try:
            with open(file_name, "r") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"File {file_name} contains invalid JSON: {e}")
        except IOError as e:
            raise IOError(f"Error reading file {file_name}: {e}")

    @staticmethod
    def append_to_json(new_data: dict, file_name: str) -> None:
        """
        Appends data to an existing JSON file.

        Parameters
        ----------
        new_data : any
            The data to append. Must be serializable to JSON.

        file_name : str
            The name of the JSON file to append the data to.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If the existing file does not contain a JSON list.
        IOError
            If there is an error writing to or reading from the file.

        Example
        -------
        >>> new_data = {"key": "new_value"}
        >>> GeneralUtils.append_to_json(new_data, "example.json")
        """
        try:
            if not os.path.exists(file_name):
                # Initialize a new file with a list containing the new data
                with open(file_name, "w") as f:
                    json.dump([new_data], f, indent=4)
            else:
                with open(file_name, "r") as f:
                    try:
                        existing_data = json.load(f)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"{file_name} contains invalid JSON: {e}")

                if not isinstance(existing_data, list):
                    raise ValueError(f"{file_name} does not contain a list to append to.")

                existing_data.append(new_data)

                with open(file_name, "w") as f:
                    json.dump(existing_data, f, indent=4)
        except TypeError as e:
            raise ValueError(f"Data is not serializable to JSON: {e}")
        except IOError as e:
            raise IOError(f"Error accessing file {file_name}: {e}")

    @staticmethod
    def clear_json_file(file_name: str) -> None:
        """
        Clears the contents of a JSON file by overwriting it with an empty list.

        Parameters
        ----------
        file_name : str
            The name of the JSON file to clear.logger_manager.py

        Returns
        -------
        None

        Raises
        ------
        IOError
            If there is an error writing to the file.

        Example
        -------
        >>> GeneralUtils.clear_json_file("example.json")
        """
        try:
            with open(file_name, "w") as f:
                json.dump([], f, indent=4)
        except IOError as e:
            raise IOError(f"Error clearing file {file_name}: {e}")
