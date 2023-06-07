from api.models import Salary, User

from .base import CRUDBase


class CRUDUser(CRUDBase):
    """Класс с запросами к таблице `user`."""
    pass


class CRUDSalary(CRUDBase):
    """Класс с запросами к таблице `salary`."""
    pass


user_crud = CRUDUser(User)
salary_crud = CRUDSalary(Salary)
