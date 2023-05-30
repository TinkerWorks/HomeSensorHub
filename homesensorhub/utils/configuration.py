"""Module responsible with the implementation of the configuration file."""
import yaml

from homesensorhub.utils import logging
logger = logging.getLogger(__name__)


class Singleton(type):
    """ A metaclass that creates a Singleton base class when called. """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Configuration(metaclass=Singleton):
    """Implements the configuration file."""

    def __init__(self, config_file: str = "./config.yaml") -> None:
        self.__config_file = config_file
        self.__config_data = self.__read()
        self.__sections_callback = {}

    def set_callback_update(self, section: str, callback_function):
        """Set the function which will be called for each section on an entry update.

        Args:
            section (str): name of the section for which the function will be called
            callback_function (function): reference to the function which will be called when an
                                          entry from the specified section is updated
        """
        self.__sections_callback[section] = callback_function

    def update_entry(self, section: str, entry: str, value: str) -> None:
        """ Updates the value of the entry from the specified section.

        Args:
            section (str): Section of the configuration file which contains the entry.
            entry (str): The name of the entry to be updated.
            value (str): The new value of the entry.
        """
        # validate the entry
        self.__config_data[section][entry] = value
        self.__write()
        logger.info("Updated %s with %s.", entry, value)

        if section in self.__sections_callback:
            self.__sections_callback[section]()
        else:
            logger.warning("Configuration update callback not implemented for %s", section)

    def section(self, section: str) -> dict:
        """ Returns the data from the requested section.

        Args:
            section (str): Name of the section for which the configuration data is retrieved.

        Returns:
            dict: The configuration data for the requested section.
        """
        if section not in self.__config_data.keys():
            self.__config_data[section] = {}
        return self.__config_data[section]

    def entry(self, section: str, entry: str, default_entry_value: str) -> str:
        """Return the value for the entry in the requested section.

        Args:
            section (str): _description_
            entry (str): _description_

        Returns:
            str: _description_
        """
        if entry not in self.section(section).keys():
            self.__config_data[section][entry] = default_entry_value
            self.__write()

        return self.__config_data[section][entry]

    def __write(self) -> None:
        """ Update the data in the configuration file. """
        with open(self.__config_file, "w", encoding="utf-8") as file:
            yaml.dump(self.__config_data, file, sort_keys=False)

    def __read(self) -> dict:
        """ Read the data from the configuration file.

        Returns:
            dict: The configuration data (sections with their entries and values).
        """
        with open(self.__config_file, "a+", encoding="utf-8") as file:
            file.seek(0)
            data = yaml.safe_load(file)
            print("Read the data from the configuration file.")
            if data:
                return data
            return {}
