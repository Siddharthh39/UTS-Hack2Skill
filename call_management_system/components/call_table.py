import reflex as rx
from call_management_system.states.call_state import CallState
from call_management_system.states.auth_state import AuthState


def status_badge(status: rx.Var[str]) -> rx.Component:
    """Renders a colored badge for the call status."""
    return rx.el.span(
        status,
        class_name=rx.match(
            status,
            (
                "Pending",
                "px-2.5 py-1 text-xs font-medium rounded-full bg-yellow-100 text-yellow-800 w-fit",
            ),
            (
                "Completed",
                "px-2.5 py-1 text-xs font-medium rounded-full bg-green-100 text-green-800 w-fit",
            ),
            (
                "Follow-up",
                "px-2.5 py-1 text-xs font-medium rounded-full bg-blue-100 text-blue-800 w-fit",
            ),
            "px-2.5 py-1 text-xs font-medium rounded-full bg-gray-100 text-gray-800 w-fit",
        ),
    )


def action_button(call: rx.Var[dict]) -> rx.Component:
    """Renders the action button based on user role and call status."""
    return rx.el.td(
        rx.cond(
            AuthState.is_admin
            & (call["assigned_to"] == ""),
            rx.el.button(
                "Assign",
                on_click=lambda: CallState.select_call_for_update(
                    call
                ),
                class_name="text-blue-600 hover:text-blue-900 font-medium text-sm",
            ),
            rx.el.button(
                "Update",
                on_click=lambda: CallState.select_call_for_update(
                    call
                ),
                class_name="text-indigo-600 hover:text-indigo-900 font-medium text-sm",
            ),
        ),
        class_name="px-6 py-4 whitespace-nowrap text-right text-sm font-medium",
    )


def call_table() -> rx.Component:
    """Renders the main table of calls."""
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Call Assignments",
                class_name="text-2xl font-bold text-gray-800",
            ),
            rx.el.div(
                rx.icon(
                    "search",
                    class_name="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400",
                ),
                rx.el.input(
                    placeholder="Search calls...",
                    default_value=CallState.search_query,
                    on_change=CallState.set_search_query.debounce(
                        300
                    ),
                    class_name="pl-10 pr-4 py-2 border border-gray-300 rounded-lg w-full max-w-xs focus:ring-2 focus:ring-indigo-500",
                ),
                class_name="relative",
            ),
            class_name="flex justify-between items-center mb-6",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Customer Name",
                            class_name="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Phone Number",
                            class_name="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Assigned To",
                            class_name="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Status",
                            class_name="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Remarks",
                            class_name="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Feedback",
                            class_name="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Actions",
                            class_name="px-6 py-3 text-right text-xs font-semibold text-gray-600 uppercase tracking-wider",
                        ),
                        class_name="bg-gray-50",
                    )
                ),
                rx.el.tbody(
                    rx.foreach(
                        CallState.filtered_calls,
                        lambda call: rx.el.tr(
                            rx.el.td(
                                call["customer_name"],
                                class_name="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900",
                            ),
                            rx.el.td(
                                call["phone_number"],
                                class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-600",
                            ),
                            rx.el.td(
                                rx.cond(
                                    call["assigned_to"]
                                    != "",
                                    rx.el.div(
                                        rx.el.img(
                                            src=f"https://api.dicebear.com/9.x/initials/svg?seed={call['assigned_to']}",
                                            class_name="h-6 w-6 rounded-full mr-2",
                                        ),
                                        rx.el.span(
                                            call[
                                                "assigned_to"
                                            ]
                                        ),
                                        class_name="flex items-center",
                                    ),
                                    rx.el.span(
                                        "Unassigned",
                                        class_name="text-gray-400 italic",
                                    ),
                                ),
                                class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-600",
                            ),
                            rx.el.td(
                                status_badge(
                                    call["status"]
                                ),
                                class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-600",
                            ),
                            rx.el.td(
                                call["remarks"],
                                class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-600 max-w-xs truncate",
                            ),
                            rx.el.td(
                                call["feedback"],
                                class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-600 max-w-xs truncate",
                            ),
                            action_button(call),
                            class_name="hover:bg-gray-50/50",
                        ),
                    ),
                    class_name="bg-white divide-y divide-gray-200",
                ),
                class_name="min-w-full divide-y divide-gray-200",
            ),
            class_name="border border-gray-200 rounded-lg overflow-x-auto shadow-sm",
        ),
        class_name="bg-white p-6 rounded-xl shadow-sm",
    )