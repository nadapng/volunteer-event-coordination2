from volunteer_event_coordination.service_layer.app_services import AppServices
from volunteer_event_coordination.application_base import ApplicationBase
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
        print(f"\t2. Add Event")
        print(f"\t3. Update User")
        print(f"\t4. Delete User")
        print()
        print(f"\t5. List all events")
        print(f"\t6. Add Event")
        print(f"\t7. Update Event")
        print(f"\t8. Delete Event")

        print(f"\t9. Register User to Event")
        print(f"\t10. Unregister User from Event")
        print()
        print(f"\t11. Exit")
        print()

    def process_menu_choice(self)->None:
        """ Process users menu choice. """
        choice = input("\tEnter your choice (1-11): ")

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
            case '10': self.unregister_user_from_event()

            case '11': sys.exit(0)

            case _: print("\tInvalid Menu choice {choice}. Please try again.")

    def list_users(self)->None:
        """ List all users. """
        print("\tListing all users...")

    def add_user(self)->None:
        """ Add a new user. """
        print("\tAdding a new user...")

    def update_user(self)->None:
        """ Update an existing user. """
        print("\tUpdating an existing user...")


    def delete_user(self)->None:
        """ Delete a user. """
        print("\tDeleting a user...")


    def list_events(self)->None:
        """ List all events. """
        print("\tListing all events...")

    def add_event(self)->None:
        """ Add a new event. """
        print("\tAdding a new event...")

    def update_event(self)->None:
        """ Update an existing event. """
        print("\tUpdating an existing event...")

    def delete_event(self)->None:
        """ Delete an event. """
        print("\tDeleting an event...")

    def register_user_to_event(self)->None:
        """ Register a user to an event. """
        print("\tRegistering a user to an event...")


    def unregister_user_from_event(self)->None:
        """ Unregister a user from an event. """
        print("\tUnregistering a user from an event...")

    def start(self)->None:
        while True:
            self.display_menu()
            self.process_menu_choice()