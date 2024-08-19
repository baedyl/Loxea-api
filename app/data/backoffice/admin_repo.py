from datetime import datetime
from datetime import timezone

from app.data.user_repo import AbstractUserRepo as BaseAbstractUserRepo
from app.data.user_repo import Session
from app.data.user_repo import User
from app.data.user_repo import UserRepo as BaseUserRepo
from app.data.user_repo import abstractmethod
from app.data.user_repo import select


class AbstractUserRepo(BaseAbstractUserRepo):

    @abstractmethod
    def get_users(): ...

    @abstractmethod
    def get_user_from_id(self, user_id: int): ...

    @abstractmethod
    def update_user(self, user_id: int): ...

    @abstractmethod
    def soft_delete_user(self, user_id: int): ...


class UserRepo(BaseUserRepo):
    def __init__(self, session: Session):
        super.__init__(session=session)

    def get_users(self) -> list[User]:
        """
        Retrieves all users who have not been marked as deleted.

        Returns:
            list[User]: A list of User objects where `is_deleted` is False.

        Notes:
            - The method queries the database for users who have the `is_deleted` flag set to False.
            - This method is useful for retrieving active users from the database.
        """
        users = self._session.exec(select(User).where(User.is_deleted == False)).all()

        return users

    def get_user_from_id(self, user_id: int) -> User | None:
        """
        Retrieves a user with the given user_id. This function does not check
        if the user has been soft deleted already.

        Args:
            user_id (int): The User ID.

        Returns:
            User | None:
                - The User object if the user has been successfully retrieved.
                - None if there's no user with the provided User ID
        """
        user = self._session.exec(select(User).where(User.id == user_id)).one_or_none()
        return user

    def soft_delete_user(self, user_id: int) -> bool:
        """
        Soft deletes a user with the given user_id by marking them as deleted.

        Args:
            user_id (int): The User ID.

        Returns:
            bool:
                - True if the user was successfully soft-deleted or was already marked as deleted.
                - False if the user was not found.
        """

        user = self.get_user_from_id(user_id)
        if not user:
            return False
        if user.is_deleted:
            return True

        user.is_deleted = True
        user.deleted_at = datetime.now(timezone.utc)
        self._session.commit()
        return True

    def update_user(self, user_id, name, email) -> User | None:
        """
        Updates the details of a user identified by the given user_id.
        This method does not verify if there is an existing user with the
        provided email.

        Args:
            user_id (int): The ID of the user to be updated.
            name (str): The new name for the user.
            email (str): The new email for the user.

        Returns:
            User | None:
                - The updated User object if the user with the given user_id exists and was updated.
                - None if no user with the given user_id was found.

        """

        user = self.get_user_from_id(user_id)
        if not user:
            return None

        user.name = name
        user.email = email
        self._session.commit()
        return user
