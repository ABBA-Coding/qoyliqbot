from aiogram import Router

from .register import router as register_router
from .payment import router as payment_router
from .callback import router as callback_router
from .echo import router as echo_router

router = Router()

router.include_router(register_router)
router.include_router(payment_router)
router.include_router(callback_router)
router.include_router(echo_router)
