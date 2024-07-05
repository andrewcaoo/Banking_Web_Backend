from fastcrud import FastCRUD

from ..models.payment import Payment 
from ..schemas.payment import PaymentCreateInternal, PaymentDelete, PaymentUpdate, PaymentUpdateInternal

CRUDPayment = FastCRUD[Payment, PaymentCreateInternal, PaymentDelete, PaymentUpdate, PaymentUpdateInternal]
crud_payment = CRUDPayment(Payment)
