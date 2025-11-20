from volunteer_event_coordination.service_layer.app_services import AppServices
from volunteer_event_coordination.application_base import ApplicationBase
from volunteer_event_coordination.infrastructure_layer.user import User
from volunteer_event_coordination.infrastructure_layer.event import Event
from prettytable import PrettyTable
import sys


class ConsoleUI(ApplicationBase):
    """ Define the ConsoleUI class. """

    def __init__(self, config:dict)->None:
        """ Initializes object. """
        self._config_dict = config
        self.META = config["meta"]
        super().__init__(subclass_name=self.__class__.__name__, 
                logfile_prefix_name=self.META["log_prefix"])
        self.app_services = AppServices(config)

    # Public Methods
    def display_menu(self)->None:
        """ Display the menu. """
        print(f"\n\t{'-'*40}")
        print(f"\tVolunteer Event Coordination System")
        print()
        print(f"\t1. List all users")
        print(f"\t2. Add User")
        print(f"\t3. Update User")
        print(f"\t4. Delete User")
        print()
        print(f"\t5. List all events")
        print(f"\t6. Add Event")
        print(f"\t7. Update Event")
        print(f"\t8. Delete Event")
        print()
        print(f"\t9. Register User to Event")
        print(f"\t10. Update User Event Registration Status")
        print(f"\t11. Unregister User from Event")
        print()
        print(f"\t12. Exit")
        print()

    def process_menu_choice(self)->None:
        """ Process users menu choice. """
        choice = input("\tEnter your choice (1-12): ")

        match choice:
            case '1': self.list_users()
            case '2': self.add_user()
            case '3': self.update_user()
            case '4': self.delete_user()

            case '5': self.list_events()
            case '6': self.add_event()
            case '7': self.update_event()
            case '8': self.delete_event()

            case '9': self.register_user_to_event()
            case '10': self.update_user_event_registration_status()
            case '11': self.unregister_user_from_event()

            case '12': sys.exit(0)

            case _: print("\tInvalid Menu choice {choice}. Please try again.")

    def list_users(self)->None:
        """ List all users. """
        print("\tListing all users...")
        users = self.app_services.get_all_users()
        users_table = PrettyTable()
        users_table.field_names = ["ID", "Full Name", "Email", "Phone", "Role", "Events"]
        events_table = PrettyTable()
        events_table.field_names = ["Title", "Starts At", "Ends At", "Location", "Capacity"]
        for student in users:
            for event in student.events:
                events_table.add_row([event.title, event.starts_at, event.ends_at, event.location, event.capacity])
            users_table.add_row([student.id, student.full_name, student.email, student.phone, student.role, events_table.get_string()])
            users_table.add_divider()
            events_table.clear_rows()
        print(users_table)

    def add_user(self)->None:
        """ Add a new user. """
        print("\tAdding a new user...")
        try:
            full_name = input("\tEnter full name: ")
            email = input("\tEnter email: ")
            phone = input("\tEnter phone: ")
            role = input("\tEnter role (volunteer/organizer): ")

            user = self.app_services.create_user(full_name, email, phone, role)
            if user:
                print(f"\tUser '{full_name}' created successfully with ID {user.id}.")
            else:
                print("\tFailed to create user.")
        except Exception as ex:
            self._logger.log_error(f"Exception occurred: {ex}")

    def update_user(self)->None:
        """ Update an existing user. """
        print("\tUpdating an existing user...")
        try:    
            user_id = int(input("\tEnter user ID to update: "))
            full_name = input("\tEnter new full name: ")
            email = input("\tEnter new email: ")
            phone = input("\tEnter new phone: ")
            role = input("\tEnter new role (volunteer/organizer): ")

            user = self.app_services.update_user(user_id, full_name, email, phone, role)
            if user:
                print(f"\tUser ID {user_id} updated successfully.")
            else:
                print(f"\tFailed to update user ID {user_id}.")
        except Exception as ex:
            self._logger.log_error(f"Exception occurred: {ex}")    

    def delete_user(self)->None:
        """ Delete a user. """
        print("\tDeleting a user...")
        try:
            user_id = int(input("\tEnter user ID to delete: "))

            success = self.app_services.delete_user(user_id)
            if success:
                print(f"\tUser ID {user_id} deleted successfully.")
            else:
                print(f"\tFailed to delete user ID {user_id}.")
        except Exception as ex:
            self._logger.log_error(f"Exception occurred: {ex}")


    def list_events(self)->None:
        """ List all events. """
        print("\tListing all events...")
        events = self.app_services.get_all_events()
        events_table = PrettyTable()
        events_table.field_names = ["ID", "Title", "Description", "Location", "Starts At", "Ends At", "Capacity", "Created By", "Created At"]
        for event in events:
            events_table.add_row([event.id, event.title, event.description, event.location, event.starts_at, event.ends_at, event.capacity, event.created_by, event.created_at])
        print(events_table)

    def add_event(self)->None:
        """ Add a new event. """
        print("\tAdding a new event...")
        try:
            title = input("\tEnter event title: ")
            description = input("\tEnter event description: ")
            location = input("\tEnter event location: ")
            starts_at = input("\tEnter event start time (YYYY-MM-DD HH:MM:SS): ")
            ends_at = input("\tEnter event end time (YYYY-MM-DD HH:MM:SS): ")
            capacity = int(input("\tEnter event capacity: "))
            created_by = int(input("\tEnter creator user ID: "))

            event = self.app_services.create_event(title, description, location, starts_at, ends_at, capacity, created_by)
            if event:
                print(f"\tEvent '{event.title}' created successfully with ID {event.id}.")
            else:
                print("\tFailed to create event.")
        except Exception as ex:
            self._logger.log_error(f"Exception occurred: {ex}")

    def update_event(self)->None:
        """ Update an existing event. """
        print("\tUpdating an existing event...")
        try:
            event_id = int(input("\tEnter event ID to update: "))
            title = input("\tEnter new event title: ")
            description = input("\tEnter new event description: ")
            location = input("\tEnter new event location: ")
            starts_at = input("\tEnter new event start time (YYYY-MM-DD HH:MM:SS): ")
            ends_at = input("\tEnter new event end time (YYYY-MM-DD HH:MM:SS): ")
            capacity = input("\tEnter new event capacity: ")

            event = self.app_services.update_event(event_id, title, description, location, starts_at, ends_at, capacity)
            if event:
                print(f"\tEvent ID {event_id} updated successfully.")
            else:
                print(f"\tFailed to update event ID {event_id}.")

        except Exception as ex:
            self._logger.log_error(f"Exception occurred: {ex}")

    def delete_event(self)->None:
        """ Delete an event. """
        print("\tDeleting an event...")
        try:
            event_id = int(input("\tEnter event ID to delete: "))

            success = self.app_services.delete_event(event_id)
            if success:
                print(f"\tEvent ID {event_id} deleted successfully.")
            else:
                print(f"\tFailed to delete event ID {event_id}.")
        except Exception as ex:
            self._logger.log_error(f"Exception occurred: {ex}")

    def register_user_to_event(self)->None:
        """ Register a user to an event. """
        print("\tRegistering a user to an event...")
        try:
            user_id = int(input("\tEnter user ID to register: "))
            event_id = int(input("\tEnter event ID to register to: "))
            status = input("\tEnter registration status (e.g., registered/waitlist/cancelled): ")
            if status not in ['registered', 'waitlist', 'cancelled']:
                status = 'registered'  # Default status

            success = self.app_services.register_user_to_event(user_id, event_id, status)
            if success:
                print(f"\tUser ID {user_id} registered to Event ID {event_id} successfully.")
            else:
                print(f"\tFailed to register User ID {user_id} to Event ID {event_id}.")

        except Exception as ex:
            self._logger.log_error(f"Exception occurred: {ex}")

    def update_user_event_registration_status(self)->None:
        """ Update a user's event registration status. """
        print("\tUpdating a user's event registration status...")
        try:
            user_id = int(input("\tEnter user ID: "))
            event_id = int(input("\tEnter event ID: "))
            status = input("\tEnter new registration status (e.g., registered/waitlist/cancelled): ")
            if status not in ['registered', 'waitlist', 'cancelled']:
                print("\tInvalid status. Please try again.")
                return

            success = self.app_services.update_user_event_registration_status(user_id, event_id, status)
            if success:
                print(f"\tUser ID {user_id} registration status for Event ID {event_id} updated to '{status}' successfully.")
            else:
                print(f"\tFailed to update registration status for User ID {user_id} and Event ID {event_id}.")

        except Exception as ex:
            self._logger.log_error(f"Exception occurred: {ex}")


    def unregister_user_from_event(self)->None:
        """ Unregister a user from an event. """
        print("\tUnregistering a user from an event...")
        try:
            user_id = int(input("\tEnter user ID to unregister: "))
            event_id = int(input("\tEnter event ID to unregister from: "))

            success = self.app_services.unregister_user_from_event(user_id, event_id)
            if success:
                print(f"\tUser ID {user_id} unregistered from Event ID {event_id} successfully.")
            else:
                print(f"\tFailed to unregister User ID {user_id} from Event ID {event_id}.")

        except Exception as ex:
            self._logger.log_error(f"Exception occurred: {ex}")

    def start(self)->None:
        while True:
            self.display_menu()
            self.process_menu_choice()