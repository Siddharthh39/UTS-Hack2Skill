import reflex as rx
from call_management_system.components.navbar import navbar
from call_management_system.components.user_dashboard import user_dashboard
from call_management_system.components.update_call_modal import (
    update_call_modal,
)


def dashboard() -> rx.Component:
    """The agent dashboard page."""
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                user_dashboard(),
                class_name="max-w-7xl mx-auto px-4 py-8",
            )
        ),
        update_call_modal(),
        class_name="bg-gray-50 min-h-screen font-['Inter']",
    )