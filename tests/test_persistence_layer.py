"""Persistence Layer Unit Tests."""
from tests.context import MySQLPersistenceWrapper
from tests.context import User
from tests.context import Event
import pytest
import json
import os
import time

@pytest.fixture(scope="class")
def mysql_persistence_wrapper():
    print(f'\nSetting up mysql_persistence_wrapper_fixture...')
    working_dir = os.getcwd()
    config_dir = 'config'
    config_file_name = 'volunteer_event_coordination_app_config.json'
    config_dir_path = os.path.join(working_dir, config_dir, config_file_name )
    config_dict = None
    with open(config_dir_path, 'r') as f:
        config_dict = json.loads(f.read())
    db = MySQLPersistenceWrapper(config_dict)
    yield db
    print(f'\nTearing down mysql_persistence_wrapper_fixture...')

class TestPersistenceLayer:
    """Persistence Layer Unit Tests."""

    # Happy Path Tests

    def test_select_all_users(self, mysql_persistence_wrapper):
        """Test: select_all_users"""
        users = mysql_persistence_wrapper.select_all_users()
        assert len(users) > 0

    def test_select_all_events(self, mysql_persistence_wrapper):
        """Test: select_all_events"""
        events = mysql_persistence_wrapper.select_all_events()
        assert len(events) > 0

    def test_select_user_by_id(self, mysql_persistence_wrapper):
        """Test: select_user_by_id"""
        # First ensure we have a user to select
        users = mysql_persistence_wrapper.select_all_users()
        if not users:
            # Create a test user if none exist
            user = User()
            user.full_name = 'Test Select User'
            user.email = f'select_{int(time.time())}@user.com'
            user.phone = '123-456-7890'
            user.role = 'volunteer'
            inserted_user = mysql_persistence_wrapper.insert_user(user)
            user_id = inserted_user.id
        else:
            user_id = users[0].id
        
        user = mysql_persistence_wrapper.select_user_by_id(user_id)
        assert user is not None

    def test_select_event_by_id(self, mysql_persistence_wrapper):
        """Test: select_event_by_id"""
        event = mysql_persistence_wrapper.select_event_by_id(1)
        assert event is not None

    def test_insert_user(self, mysql_persistence_wrapper):
        """Test: insert_user"""
        user = User()
        user.full_name = 'Test User'
        # Use timestamp to ensure unique email for each test run
        user.email = f'test_{int(time.time())}@user.com'
        user.phone = '123-456-7890'
        user.role = 'volunteer'
        inserted_user = mysql_persistence_wrapper.insert_user(user)
        assert inserted_user is not None

    def test_insert_event(self, mysql_persistence_wrapper):
        """Test: insert_event"""
        # First ensure we have a user to reference
        users = mysql_persistence_wrapper.select_all_users()
        if not users:
            # Create a test user if none exist
            user = User()
            user.full_name = 'Event Creator'
            user.email = f'creator_{int(time.time())}@user.com'
            user.phone = '123-456-7890'
            user.role = 'organizer'
            inserted_user = mysql_persistence_wrapper.insert_user(user)
            user_id = inserted_user.id
        else:
            user_id = users[0].id
            
        event = Event()
        event.title = 'Test Event'
        event.description = 'This is a test event.'
        event.location = 'Test Location'
        event.starts_at = '2024-07-01 10:00:00'
        event.ends_at = '2024-07-01 12:00:00'
        event.capacity = 50
        event.created_by = user_id
        inserted_event = mysql_persistence_wrapper.insert_event(event)
        assert inserted_event is not None

    def test_update_user(self, mysql_persistence_wrapper):
        """Test: update_user"""
        # First ensure we have a user to update
        users = mysql_persistence_wrapper.select_all_users()
        if not users:
            # Create a test user if none exist
            user = User()
            user.full_name = 'Update Test User'
            user.email = f'update_{int(time.time())}@user.com'
            user.phone = '123-456-7890'
            user.role = 'volunteer'
            inserted_user = mysql_persistence_wrapper.insert_user(user)
            user_id = inserted_user.id
        else:
            user_id = users[0].id
            
        user = mysql_persistence_wrapper.select_user_by_id(user_id)
        user.full_name = 'Updated user name'
        
        mysql_persistence_wrapper.update_user(user)
        updated_user = mysql_persistence_wrapper.select_user_by_id(user_id)
        assert updated_user.full_name == 'Updated user name'

    def test_delete_user(self, mysql_persistence_wrapper):
        """Test: delete_user"""
        user = User()
        user.full_name = 'Delete Test User'
        # Use timestamp to ensure unique email for each test run
        user.email = f'deleted_{int(time.time())}@user.com'
        user.phone = '987-654-3210'
        user.role = 'volunteer'
        inserted_user = mysql_persistence_wrapper.insert_user(user)
        mysql_persistence_wrapper.delete_user(inserted_user.id)
        deleted_user = mysql_persistence_wrapper.select_user_by_id(inserted_user.id)
        assert deleted_user is None

    # Edge Case Tests
    def test_select_user_by_invalid_id(self, mysql_persistence_wrapper):
        """Test: select_user_by_invalid_id"""
        user = mysql_persistence_wrapper.select_user_by_id(0)
        assert user is None

    def test_select_event_by_invalid_id(self, mysql_persistence_wrapper):
        """Test: select_event_by_invalid_id"""
        event = mysql_persistence_wrapper.select_event_by_id(0)
        assert event is None

    def test_delete_nonexistent_user(self, mysql_persistence_wrapper):
        """Test: delete_nonexistent_user"""
        mysql_persistence_wrapper.delete_user(99999)
        assert True  # No exception means pass

    def test_delete_nonexistent_event(self, mysql_persistence_wrapper):
        """Test: delete_nonexistent_event"""
        mysql_persistence_wrapper.delete_event(99999)
        assert True  # No exception means pass