from .base import CRUDBase
from app.models import Salary, User

class CRUDUser(CRUDBase):
    """Класс с запросами к таблице `user`."""
    pass

class CRUDSalary(CRUDBase):
    """Класс с запросами к таблице `salary`."""
    pass

user_crud = CRUDUser(User)
salary_crud = CRUDSalary(Salary)