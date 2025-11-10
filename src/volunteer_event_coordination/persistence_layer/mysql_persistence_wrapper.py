"""Defines the MySQLPersistenceWrapper class."""

from volunteer_event_coordination.application_base import ApplicationBase
from mysql import connector
from mysql.connector.pooling import (MySQLConnectionPool)
import inspect
import json
from enum import Enum
from volunteer_event_coordination.infrastructure_layer.user import User
from volunteer_event_coordination.infrastructure_layer.event import Event
from typing import List

class MySQLPersistenceWrapper(ApplicationBase):
	"""Implements the MySQLPersistenceWrapper class."""

	def __init__(self, config:dict)->None:
		"""Initializes object. """
		self._config_dict = config
		self.META = config["meta"]
		self.DATABASE = config["database"]
		super().__init__(subclass_name=self.__class__.__name__, 
				   logfile_prefix_name=self.META["log_prefix"])
		self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}:It works!')

		# Database Configuration Constants
		self.DB_CONFIG = {}
		self.DB_CONFIG['database'] = \
			self.DATABASE["connection"]["config"]["database"]
		self.DB_CONFIG['user'] = self.DATABASE["connection"]["config"]["user"]
		self.DB_CONFIG['password'] = self.DATABASE["connection"]["config"]['password']
		self.DB_CONFIG['host'] = self.DATABASE["connection"]["config"]["host"]
		self.DB_CONFIG['port'] = self.DATABASE["connection"]["config"]["port"]

		self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: DB Connection Config Dict: {self.DB_CONFIG}')

		# Database Connection
		self._connection_pool = \
			self._initialize_database_connection_pool(self.DB_CONFIG)
		
		# Model Column ENUM Constants
		self.UserColumns = \
			Enum('UserColumns',[ ('id', 0), ('full_name', 1), ('email', 2), ('phone', 3), ('role', 4), ('created_at', 5)])

		self.EventColumns = \
			Enum('EventColumns',[ ('id', 0), ('title', 1), ('description', 2), ('location', 3), ('starts_at', 4), ('ends_at', 5), ('capacity', 6), ('created_by', 7), ('created_at', 8)])
	

		# SQL String Constants
		self.SELECT_ALL_USERS = \
			"SELECT id, full_name, email, phone, role, created_at "\
			"FROM users;"
		
		self.SELECT_ALL_EVENTS = \
			"SELECT id, title, description, location, starts_at, ends_at, capacity, created_by, created_at "\
			"FROM events;"
		
		self.SELECT_USER_BY_ID = \
			"SELECT id, full_name, email, phone, role, created_at "\
			"FROM users "\
			"WHERE id = %s;"
		
		self.SELECT_EVENT_BY_ID = \
			"SELECT id, title, description, location, starts_at, ends_at, capacity, created_by, created_at "\
			"FROM events "\
			"WHERE id = %s;"
		
		self.SELECT_REGISTERED_EVENTS_FOR_USER_ID = \
			"SELECT e.id, e.title, e.description, e.location, e.starts_at, e.ends_at, e.capacity, e.created_by, e.created_at "\
			"FROM events e , volunteer_shift_xref x "\
			"WHERE e.id = x.event_id AND x.user_id = %s;"
		
		self.INSERT_USER = \
			"INSERT INTO users (full_name, email, phone, role) "\
			"VALUES (%s, %s, %s, %s);"
		
		self.INSERT_EVENT = \
			"INSERT INTO events (title, description, location, starts_at, ends_at, capacity, created_by) "\
			"VALUES (%s, %s, %s, %s, %s, %s, %s);"
		
		self.UPDATE_USER = \
			"UPDATE users "\
			"SET full_name = %s, email = %s, phone = %s, role = %s "\
			"WHERE id = %s;"
		
		self.UPDATE_EVENT = \
			"UPDATE events "\
			"SET title = %s, description = %s, location = %s, starts_at = %s, ends_at = %s, capacity = %s "\
			"WHERE id = %s;"


	# MySQLPersistenceWrapper Methods
	def select_all_users(self)->List[User]:
		"""Selects all users from the database."""
		cursor = None
		results = None
		users_list = []
		try:
			connection = self._connection_pool.get_connection()
			with connection:
				cursor = connection.cursor()
				with cursor:
					cursor.execute(self.SELECT_ALL_USERS)
					results = cursor.fetchall()
				users_list = self._pupulate_user_objects(results)
			for user in users_list:
				events_list = self.select_all_events_for_user_id(user.id) or []
				user.events = self._populate_event_objects(events_list)
				self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: Retrieved user')

			return users_list
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: Problem selecting all users: {e}')
			return []
	
	def select_all_events(self)->List[Event]:
		"""Selects all events from the database."""
		cursor = None
		results = None
		try:
			connection = self._connection_pool.get_connection()
			with connection:
				cursor = connection.cursor()
				with cursor:
					cursor.execute(self.SELECT_ALL_EVENTS)
					results = cursor.fetchall()
			return self._populate_event_objects(results)
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: Problem selecting all events: {e}')
			return []
		
	def select_user_by_id(self, user_id:int)->User:
		"""Selects a user by ID from the database."""
		cursor = None
		result = None
		try:
			connection = self._connection_pool.get_connection()
			with connection:
				cursor = connection.cursor()
				with cursor:
					cursor.execute(self.SELECT_USER_BY_ID, (user_id,))
					result = cursor.fetchone()
			if result:
				users_list = self._pupulate_user_objects([result])
				if users_list:
					user = users_list[0]
					events_list = self.select_all_events_for_user_id(user.id) or []
					user.events = self._populate_event_objects(events_list)
					return user
			return None
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: Problem selecting user by ID {user_id}: {e}')
			return None
		
	def select_event_by_id(self, event_id:int)->Event:
		"""Selects an event by ID from the database."""
		cursor = None
		result = None
		try:
			connection = self._connection_pool.get_connection()
			with connection:
				cursor = connection.cursor()
				with cursor:
					cursor.execute(self.SELECT_EVENT_BY_ID, (event_id,))
					result = cursor.fetchone()
			if result:
				events_list = self._populate_event_objects([result])
				if events_list:
					return events_list[0]
			return None
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: Problem selecting event by ID {event_id}: {e}')
			return None
	
	def select_all_events_for_user_id(self, user_id:int)->List[Event]:
		"""Selects all events for a given user ID from the database."""
		cursor = None
		results = None
		try:
			connection = self._connection_pool.get_connection()
			with connection:
				cursor = connection.cursor()
				with cursor:
					cursor.execute(self.SELECT_REGISTERED_EVENTS_FOR_USER_ID, (user_id,))
					results = cursor.fetchall()
			return results
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: Problem selecting all modules for user ID {user_id}: {e}')
			return []

	def insert_user(self, user:User)->User:
		"""Inserts a new user into the database."""
		cursor = None
		try:
			connection = self._connection_pool.get_connection()
			with connection:
				cursor = connection.cursor()
				with cursor:
					cursor.execute(self.INSERT_USER, (user.full_name, user.email, user.phone, user.role))
					connection.commit()
			return User
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: Problem inserting user: {e}')
			return None
		
	def insert_event(self, event:Event)->Event:
		"""Inserts a new event into the database."""
		cursor = None
		try:
			connection = self._connection_pool.get_connection()
			with connection:
				cursor = connection.cursor()
				with cursor:
					cursor.execute(self.INSERT_EVENT, (event.title, event.description, event.location, event.starts_at, event.ends_at, event.capacity, event.created_by))
					connection.commit()
			return event
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: Problem inserting event: {e}')
			return None

	def update_user(self, user:User)->bool:
		"""Updates an existing user in the database."""
		cursor = None
		try:
			connection = self._connection_pool.get_connection()
			with connection:
				cursor = connection.cursor()
				with cursor:
					cursor.execute(self.UPDATE_USER, (user.full_name, user.email, user.phone, user.role, user.id))
					connection.commit()
			return True
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: Problem updating user: {e}')
			return False
		
	def update_event(self, event:Event)->bool:
		"""Updates an existing event in the database."""
		cursor = None
		try:
			connection = self._connection_pool.get_connection()
			with connection:
				cursor = connection.cursor()
				with cursor:
					cursor.execute(self.UPDATE_EVENT, (event.title, event.description, event.location, event.starts_at, event.ends_at, event.capacity, event.id))
					connection.commit()
			return True
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: Problem updating event: {e}')
			return False



	##### Private Utility Methods #####

	def _initialize_database_connection_pool(self, config:dict)->MySQLConnectionPool:
		"""Initializes database connection pool."""
		try:
			self._logger.log_debug(f'Creating connection pool...')
			cnx_pool = \
				MySQLConnectionPool(pool_name = self.DATABASE["pool"]["name"],
					pool_size=self.DATABASE["pool"]["size"],
					pool_reset_session=self.DATABASE["pool"]["reset_session"],
					use_pure=self.DATABASE["pool"]["use_pure"],
					**config)
			self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: Connection pool successfully created!')
			return cnx_pool
		except connector.Error as err:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: Problem creating connection pool: {err}')
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: Check DB cnfg:\n{json.dumps(self.DATABASE)}')
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}:Problem creating connection pool: {e}')
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}:Check DB conf:\n{json.dumps(self.DATABASE)}')

	def _pupulate_user_objects(self, results:List)->List[User]:
		"""Populates and returns a list of user objects."""
		users_list = []
		try:
			for row in results:
				user = User()
				user.id = row[self.UserColumns['id'].value]
				user.full_name = row[self.UserColumns['full_name'].value]
				user.email = row[self.UserColumns['email'].value]
				user.phone = row[self.UserColumns['phone'].value]
				user.role = row[self.UserColumns['role'].value]
				user.created_at = row[self.UserColumns['created_at'].value]
				users_list.append(user)
			return users_list
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: Problem populating user objects: {e}')
			return []
		
	def _populate_event_objects(self, results:List)->List[Event]:
		"""Populates and returns a list of event objects."""
		events_list = []
		try:
			for row in results:
				event = Event()
				event.id = row[self.EventColumns['id'].value]
				event.title = row[self.EventColumns['title'].value]
				event.description = row[self.EventColumns['description'].value]
				event.location = row[self.EventColumns['location'].value]
				event.starts_at = row[self.EventColumns['starts_at'].value]
				event.ends_at = row[self.EventColumns['ends_at'].value]
				event.capacity = row[self.EventColumns['capacity'].value]
				event.created_by = row[self.EventColumns['created_by'].value]
				event.created_at = row[self.EventColumns['created_at'].value]
				events_list.append(event)
			return events_list
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: Problem populating event objects: {e}')
			return []