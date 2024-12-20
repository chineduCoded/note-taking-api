from typing import Protocol


class UserManager(Protocol):
    def login(self, username: str, password: str) -> bool:
        """Login the user"""
        pass

    def logout(self) -> None:
        """Logout the user"""
        pass

    def register(self, username: str, password: str) -> bool:
        """Register the user"""
        pass