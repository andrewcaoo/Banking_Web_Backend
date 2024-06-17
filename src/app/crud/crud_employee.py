from fastcrud import FastCRUD

from ..models.employee import Employee 
from ..schemas.employee import EmployeeCreateInternal, EmployeeDelete, EmployeeUpdate, EmployeeUpdateInternal

CRUDEmployee = FastCRUD[Employee, EmployeeCreateInternal, EmployeeDelete, EmployeeUpdate, EmployeeUpdateInternal]
crud_employee = CRUDEmployee(Employee)
