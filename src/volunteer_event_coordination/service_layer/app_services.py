"""Implements AppServices Class."""

from volunteer_event_coordination.application_base import ApplicationBase
from volunteer_event_coordination.persistence_layer.mysql_persistence_wrapper import MySQLPersistenceWrapper
from volunteer_event_coordination.infrastructure_layer.user import User
from volunteer_event_coordination.infrastructure_layer.event import Event
from typing import List
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
    
    def get_all_users(self)->List[User]:
        """ Return a list of user objects. """

        self._logger.log_debug(f"{inspect.currentframe().f_code.co_name}: Retrieving all users from database.")
        user_dict = {}
        user_dict['users'] = []

        try:
            results = self.DB.select_all_users()
            return results
        except Exception as ex:
            self._logger.log_error(f"{inspect.currentframe().f_code.co_name}: Exception occurred: {ex}")

    def get_all_events(self)->List[Event]:
        """ Return a list of event objects. """

        self._logger.log_debug(f"{inspect.currentframe().f_code.co_name}: Retrieving all events from database.")
        event_dict = {}
        event_dict['events'] = []

        try:
            results = self.DB.select_all_events()
            return results
        except Exception as ex:
            self._logger.log_error(f"{inspect.currentframe().f_code.co_name}: Exception occurred: {ex}")

    def get_user_by_id(self, user_id:int)->User:
        """ Return a user object by ID. """

        self._logger.log_debug(f"{inspect.currentframe().f_code.co_name}: Retrieving user id {user_id} from database.")

        try:
            result = self.DB.select_user_by_id(user_id)
            return result
        except Exception as ex:
            self._logger.log_error(f"{inspect.currentframe().f_code.co_name}: Exception occurred: {ex}")
            return None

    def get_event_by_id(self, event_id:int)->Event:
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
        
    def create_user(self, full_name:str, email:str, phone:str, role:str)->User:
        """ Create a new user in the database. """

        self._logger.log_debug(f"{inspect.currentframe().f_code.co_name}: Creating new user {full_name}.")

        try:
            user = User()
            user.full_name = full_name
            user.email = email
            user.phone = phone
            user.role = role
            inserted_user = self.DB.insert_user(user)
            if inserted_user:
                return user
            return None
        except Exception as ex:
            self._logger.log_error(f"{inspect.currentframe().f_code.co_name}: Exception occurred: {ex}")
            return None
        
    def create_event(self, title:str, description:str, location:str, starts_at:str, ends_at:str, capacity:int, created_by:int):
        """ Create a new event in the database. """

        self._logger.log_debug(f"{inspect.currentframe().f_code.co_name}: Creating new event {title}.")

        try:
            user = self.DB.select_user_by_id(created_by)
            if not user:
                self._logger.log_error(f"{inspect.currentframe().f_code.co_name}: Creator user id {created_by} does not exist.")
                return None
            event = Event()
            event.title = title
            event.description = description
            event.location = location
            event.starts_at = starts_at
            event.ends_at = ends_at
            event.capacity = capacity
            event.created_by = created_by
            inserted_event = self.DB.insert_event(event)
            if inserted_event:
                return event
            return None
        except Exception as ex:
            self._logger.log_error(f"{inspect.currentframe().f_code.co_name}: Exception occurred: {ex}")
            return None

    def update_user(self, user_id:int, full_name:str, email:str, phone:str, role:str)->User:
        """ Update an existing user in the database. """

        self._logger.log_debug(f"{inspect.currentframe().f_code.co_name}: Updating user id {user_id}.")

        try:
            user = self.DB.select_user_by_id(user_id)
            if not user:
                self._logger.log_error(f"{inspect.currentframe().f_code.co_name}: User id {user_id} does not exist.")
                return False
            if full_name != "": user.full_name = full_name
            if email != "": user.email = email
            if phone != "": user.phone = phone
            if role != "": user.role = role
            updated_user = self.DB.update_user(user)
            if updated_user is None:
                return None
            return user
        except Exception as ex:
            self._logger.log_error(f"{inspect.currentframe().f_code.co_name}: Exception occurred: {ex}")
            return None

    def update_event(self, event_id:int, title:str, description:str, location:str, starts_at:str, ends_at:str, capacity:str)->Event:
        """ Update an existing event in the database. """

        self._logger.log_debug(f"{inspect.currentframe().f_code.co_name}: Updating event id {event_id}.")

        try:
            event = self.DB.select_event_by_id(event_id)
            if not event:
                self._logger.log_error(f"{inspect.currentframe().f_code.co_name}: Event id {event_id} does not exist.")
                return False
            if title != "": event.title = title
            if description != "": event.description = description
            if location != "": event.location = location
            if starts_at != "": event.starts_at = starts_at
            if ends_at != "": event.ends_at = ends_at
            if capacity != "": event.capacity = int(capacity)
            updated_event = self.DB.update_event(event)
            if updated_event is None:
                return None
            return event
        except Exception as ex:
            self._logger.log_error(f"{inspect.currentframe().f_code.co_name}: Exception occurred: {ex}")
            return None
        
    def delete_user(self, user_id:int)->bool:
        """ Delete a user from the database. """

        self._logger.log_debug(f"{inspect.currentframe().f_code.co_name}: Deleting user id {user_id}.")

        try:
            user = self.DB.select_user_by_id(user_id)
            if not user:
                self._logger.log_error(f"{inspect.currentframe().f_code.co_name}: User id {user_id} does not exist.")
                return False
            deleted = self.DB.delete_user(user_id)
            return deleted
        except Exception as ex:
            self._logger.log_error(f"{inspect.currentframe().f_code.co_name}: Exception occurred: {ex}")
            return False
        
    def delete_event(self, event_id:int)->bool:
        """ Delete an event from the database. """

        self._logger.log_debug(f"{inspect.currentframe().f_code.co_name}: Deleting event id {event_id}.")

        try:
            event = self.DB.select_event_by_id(event_id)
            if not event:
                self._logger.log_error(f"{inspect.currentframe().f_code.co_name}: Event id {event_id} does not exist.")
                return False
            deleted = self.DB.delete_event(event_id)
            return deleted
        except Exception as ex:
            self._logger.log_error(f"{inspect.currentframe().f_code.co_name}: Exception occurred: {ex}")
            return False

