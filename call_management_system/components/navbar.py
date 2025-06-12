import reflex as rx
from call_management_system.states.call_state import CallState
from call_management_system.states.auth_state import AuthState


def navbar() -> rx.Component:
    """Renders the navigation bar."""
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "phone-call",
                    class_name="h-6 w-6 text-indigo-600",
                ),
                rx.el.p(
                    "UTS Call Center",
                    class_name="text-xl font-bold text-gray-800",
                ),
                class_name="flex items-center gap-3",
            ),
            rx.el.div(
                rx.cond(
                    AuthState.is_admin,
                    rx.el.div(
                        rx.el.button(
                            rx.icon(
                                "cloud_upload",
                                class_name="mr-2 h-4 w-4",
                            ),
                            "Upload CSV",
                            on_click=CallState.toggle_upload_modal,
                            class_name="flex items-center bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 transition-colors font-medium text-sm",
                        ),
                        rx.el.button(
                            rx.icon(
                                "cloud_download",
                                class_name="mr-2 h-4 w-4",
                            ),
                            "Download Data",
                            on_click=CallState.export_data,
                            class_name="flex items-center bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition-colors font-medium text-sm",
                        ),
                        class_name="flex items-center gap-4",
                    ),
                    rx.fragment(),
                ),
                rx.el.div(
                    rx.el.p(
                        f"Welcome, {AuthState.logged_in_user_email}",
                        class_name="text-sm text-gray-600 font-medium",
                    ),
                    rx.el.button(
                        "Sign Out",
                        on_click=AuthState.sign_out,
                        class_name="bg-red-500 text-white px-3 py-1.5 rounded-lg hover:bg-red-600 transition-colors text-sm font-medium",
                    ),
                    class_name="flex items-center gap-4",
                ),
                class_name="flex items-center gap-4",
            ),
            class_name="flex items-center justify-between w-full max-w-7xl mx-auto px-4",
        ),
        class_name="w-full py-4 border-b border-gray-200 bg-white/80 backdrop-blur-sm sticky top-0 z-10",
    )