from fastapi import APIRouter

from .login import router as login_router
from .logout import router as logout_router
from .tiers import router as tiers_router
from .base_account import router as base_account_router
from .employee import router as employee_router
from .branch import router as branch_router
from .customer import router as customer_router
from .loan import router as loan_router
from .region import router as region_router
from .payment import router as payment_router
from .cus_account import router as cus_account_router
from .loan_type import router as loan_type_router
from .transaction import router as transaction_router
from .online_transaction import router as online_transaction_router


router = APIRouter(prefix="/v1")
router.include_router(login_router)
router.include_router(logout_router)
router.include_router(base_account_router)
router.include_router(employee_router)
router.include_router(branch_router)
router.include_router(customer_router)
router.include_router(loan_router)
router.include_router(region_router)
router.include_router(payment_router)
router.include_router(cus_account_router)
router.include_router(loan_type_router)
router.include_router(transaction_router)
router.include_router(online_transaction_router)