import reflex as rx
from call_management_system.components.login_card import login_card


def login() -> rx.Component:
    """The login page for the app."""
    return rx.el.div(
        login_card(),
        class_name="flex items-center justify-center min-h-screen bg-gray-100 p-4",
    )