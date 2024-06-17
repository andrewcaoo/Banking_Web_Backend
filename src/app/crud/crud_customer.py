from fastcrud import FastCRUD

from ..models.customer import Customer 
from ..schemas.customer import CustomerCreateInternal, CustomerDelete, CustomerUpdate, CustomerUpdateInternal 

CRUDCustomer = FastCRUD[Customer, CustomerCreateInternal, CustomerDelete, CustomerUpdate, CustomerUpdateInternal]
crud_customer = CRUDCustomer(Customer)
