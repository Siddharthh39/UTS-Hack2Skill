import reflex as rx
from call_management_system.pages.login import login
from call_management_system.pages.admin import admin
from call_management_system.pages.dashboard import dashboard
from call_management_system.states.auth_state import AuthState


def index() -> rx.Component:
    """The index page that redirects based on auth status."""
    return rx.el.div(
        rx.el.p("Loading..."),
        class_name="flex items-center justify-center min-h-screen bg-gray-100",
    )


# Initialize the Reflex app with theme and routes.
app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(
            rel="preconnect",
            href="https://fonts.googleapis.com",
        ),
        rx.el.link(
            rel="preconnect",
            href="https://fonts.gstatic.com",
            crossorigin="",
        ),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(
    index,
    route="/",
    on_load=AuthState.check_login_and_redirect,
)
app.add_page(login, route="/login")
app.add_page(
    admin,
    route="/admin",
    on_load=AuthState.check_admin_access,
)
app.add_page(
    dashboard,
    route="/dashboard",
    on_load=AuthState.check_agent_access,
)