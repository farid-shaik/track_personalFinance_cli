import fire
import os
from user import create_user, authenticate_user

class UserLoginSystem:
    def __init__(self):
        self.logged_in_user = None

    def create_user(self, username, password):
        """Create a new user."""
        return create_user(username, password)

    def authenticate_user(self, username, password):
        """Authenticate an existing user."""
        result = authenticate_user(username, password)
        if "successful" in result:
            self.logged_in_user = username
            self.custom_prompt()
        else:
            print("username or password not exits")
        # return result

    def logout(self):
        """Logout the current user."""
        self.logged_in_user = None
        print("Logged out successfully!")
        # self.custom_prompt()

    def custom_prompt(self):
        """Simulate a custom prompt."""
        if self.logged_in_user:
            prompt = f'{self.logged_in_user}@CLI: '
        else:
            print("username or password not exits")
        while True:
            command = input(prompt)
            if command == 'logout':
                self.logout()
                break
            if command == 'annual report':
                print("your savings are one lakh rupees")
            else:
                print(f'Executing command: {command}')

if __name__ == '__main__':
    fire.Fire(UserLoginSystem)
