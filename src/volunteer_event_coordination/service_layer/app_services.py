"""Implements AppServices Class."""

from volunteer_event_coordination.application_base import ApplicationBase
from volunteer_event_coordination.persistence_layer.mysql_persistence_wrapper import MySQLPersistenceWrapper
import inspect

class AppServices(ApplicationBase):
    """AppServices Class Definition."""
    def __init__(self, config:dict)->None:
        """Initializes object. """
        self._config_dict = config
        self.META = config["meta"]
        super().__init__(subclass_name=self.__class__.__name__, 
				   logfile_prefix_name=self.META["log_prefix"])
        self.DB = MySQLPersistenceWrapper(config)
        self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}:It works!')
    
    def get_all_users(self):
        """ Return a list of user objects. """

        self._logger.log_debug(f"{inspect.currentframe().f_code.co_name}: Retrieving all users from database.")
        user_dict = {}
        user_dict['users'] = []

        try:
            results = self.DB.select_all_users()
            return results
        except Exception as ex:
            self._logger.log_error(f"{inspect.currentframe().f_code.co_name}: Exception occurred: {ex}")

    def get_all_events(self):
        """ Return a list of event objects. """

        self._logger.log_debug(f"{inspect.currentframe().f_code.co_name}: Retrieving all events from database.")
        event_dict = {}
        event_dict['events'] = []

        try:
            results = self.DB.select_all_events()
            return results
        except Exception as ex:
            self._logger.log_error(f"{inspect.currentframe().f_code.co_name}: Exception occurred: {ex}")

    def get_user_by_id(self, user_id:int):
        """ Return a user object by ID. """

        self._logger.log_debug(f"{inspect.currentframe().f_code.co_name}: Retrieving user id {user_id} from database.")

        try:
            result = self.DB.select_user_by_id(user_id)
            return result
        except Exception as ex:
            self._logger.log_error(f"{inspect.currentframe().f_code.co_name}: Exception occurred: {ex}")
            return None

    def get_event_by_id(self, event_id:int):
        """ Return an event object by ID. """

        self._logger.log_debug(f"{inspect.currentframe().f_code.co_name}: Retrieving event id {event_id} from database.")

        try:
            result = self.DB.select_event_by_id(event_id)
            return result
        except Exception as ex:
            self._logger.log_error(f"{inspect.currentframe().f_code.co_name}: Exception occurred: {ex}")
            return None
    
    def get_registered_events_for_user_id(self, user_id:int):
        """ Return a list of event objects for a given user ID. """

        self._logger.log_debug(f"{inspect.currentframe().f_code.co_name}: Retrieving registered events for user id {user_id} from database.")

        try:
            results = self.DB.select_all_events_for_user_id(user_id)
            return results
        except Exception as ex:
            self._logger.log_error(f"{inspect.currentframe().f_code.co_name}: Exception occurred: {ex}")
            return []
