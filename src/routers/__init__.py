from .menu import menu_router
from .support import support_router
from .cart import cart_router
from .history import history_router
from .catalog import catalog_router

routers = [
    menu_router,
    support_router,
    cart_router,
    history_router,
    catalog_router
]