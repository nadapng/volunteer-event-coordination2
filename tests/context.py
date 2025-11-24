import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/')))

from volunteer_event_coordination.persistence_layer.mysql_persistence_wrapper import MySQLPersistenceWrapper
from volunteer_event_coordination.service_layer.app_services import AppServices
from volunteer_event_coordination.infrastructure_layer.user import User
from volunteer_event_coordination.infrastructure_layer.event import Event