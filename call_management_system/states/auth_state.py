import reflex as rx
from typing import TypedDict


class User(TypedDict):
    password: str
    role: str


class AuthState(rx.State):
    """The authentication state for the app."""

    users: dict[str, User] = {
        "admin@hack2skill": {
            "password": "admin",
            "role": "admin",
        },
        "mayank.verma@hack2skill": {
            "password": "password",
            "role": "agent",
        },
        "priyanshu.singh@hack2skill": {
            "password": "password",
            "role": "agent",
        },
        "satyam.kumar@hack2skill": {
            "password": "password",
            "role": "agent",
        },
    }
    logged_in_user_email: str = ""
    in_session: bool = False

    @rx.var
    def get_current_user_role(self) -> str:
        """Returns the role of the currently logged-in user."""
        user = self.users.get(self.logged_in_user_email)
        if user:
            return user["role"]
        return ""

    @rx.var
    def is_admin(self) -> bool:
        """Checks if the current user is an admin."""
        return self.get_current_user_role == "admin"

    @rx.event
    def sign_in(self, form_data: dict):
        """Signs in a user."""
        email = form_data["email"]
        password = form_data["password"]
        user = self.users.get(email)
        if user and user["password"] == password:
            self.logged_in_user_email = email
            self.in_session = True
            yield rx.redirect("/")
        else:
            self.in_session = False
            yield rx.toast.error(
                "Invalid email or password."
            )

    @rx.event
    def sign_out(self):
        """Signs out a user."""
        self.in_session = False
        self.logged_in_user_email = ""
        return rx.redirect("/login")

    @rx.event
    def check_session(self):
        """Checks if a user is in session, otherwise redirects to login."""
        if not self.in_session:
            return rx.redirect("/login")

    @rx.event
    def check_login_and_redirect(self):
        """Redirects user based on their role if logged in."""
        if not self.in_session:
            return rx.redirect("/login")
        if self.is_admin:
            return rx.redirect("/admin")
        else:
            return rx.redirect("/dashboard")

    @rx.event
    def check_admin_access(self):
        """Protects admin pages."""
        if not self.in_session:
            return rx.redirect("/login")
        if not self.is_admin:
            yield rx.toast.error("Unauthorized access.")
            return rx.redirect("/dashboard")

    @rx.event
    def check_agent_access(self):
        """Protects agent pages."""
        if not self.in_session:
            return rx.redirect("/login")
        if self.is_admin:
            yield rx.toast.error(
                "Redirecting to admin dashboard."
            )
            return rx.redirect("/admin")