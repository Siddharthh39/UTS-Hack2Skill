import reflex as rx
from call_management_system.states.auth_state import AuthState


def login_card() -> rx.Component:
    """Renders the login card component."""
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Sign in to your account",
                class_name="font-semibold tracking-tight text-2xl",
            ),
            rx.el.p(
                "Enter your credentials to access the call center.",
                class_name="text-sm text-gray-500 font-medium",
            ),
            class_name="flex flex-col text-center",
        ),
        rx.el.form(
            rx.el.div(
                rx.el.label(
                    "Email",
                    html_for="email",
                    class_name="text-sm font-medium leading-none",
                ),
                rx.el.input(
                    type="email",
                    placeholder="user@hack2skill",
                    id="email",
                    name="email",
                    required=True,
                    class_name="flex h-10 w-full rounded-md border bg-transparent px-3 py-2 text-base shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 md:text-sm font-medium",
                ),
                class_name="flex flex-col gap-1.5",
            ),
            rx.el.div(
                rx.el.label(
                    "Password",
                    html_for="password",
                    class_name="text-sm font-medium leading-none",
                ),
                rx.el.input(
                    type="password",
                    id="password",
                    name="password",
                    required=True,
                    class_name="flex h-10 w-full rounded-md border bg-transparent px-3 py-2 text-base shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 md:text-sm font-medium",
                ),
                class_name="flex flex-col gap-1.5",
            ),
            rx.el.button(
                "Sign in",
                type="submit",
                class_name="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors text-white shadow bg-indigo-600 hover:bg-indigo-700 h-10 px-4 py-2 w-full mt-2",
            ),
            class_name="flex flex-col gap-4",
            on_submit=AuthState.sign_in,
            reset_on_submit=True,
        ),
        class_name="p-8 rounded-xl bg-white flex flex-col gap-6 shadow-sm border border-gray-200 text-black w-full max-w-md",
    )