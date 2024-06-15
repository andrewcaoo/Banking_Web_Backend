from fastapi import APIRouter

from .login import router as login_router
from .logout import router as logout_router
from .rate_limits import router as rate_limits_router
from .tiers import router as tiers_router
from .base_account import router as base_account_router

router = APIRouter(prefix="/v1")
router.include_router(login_router)
router.include_router(logout_router)
router.include_router(base_account_router)
# router.include_router(tiers_router)
# router.include_router(rate_limits_router)
