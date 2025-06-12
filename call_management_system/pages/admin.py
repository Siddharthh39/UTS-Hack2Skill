import reflex as rx
from call_management_system.components.navbar import navbar
from call_management_system.components.admin_dashboard import admin_dashboard
from call_management_system.components.call_table import call_table
from call_management_system.components.upload_modal import upload_modal
from call_management_system.components.update_call_modal import (
    update_call_modal,
)


def admin() -> rx.Component:
    """The admin dashboard page."""
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                admin_dashboard(),
                call_table(),
                class_name="space-y-8",
            ),
            class_name="max-w-7xl mx-auto px-4 py-8",
        ),
        upload_modal(),
        update_call_modal(),
        class_name="bg-gray-50 min-h-screen font-['Inter']",
    )