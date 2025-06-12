import reflex as rx
from call_management_system.states.call_state import CallState
from call_management_system.states.auth_state import AuthState


def update_call_modal() -> rx.Component:
    """Renders the modal for updating a call."""
    return rx.el.dialog(
        rx.cond(
            CallState.selected_call,
            rx.el.form(
                rx.el.div(
                    rx.el.h3(
                        "Update Call Details",
                        class_name="text-lg font-semibold text-gray-800",
                    ),
                    rx.el.p(
                        f"Updating call for: {CallState.selected_call['customer_name']}",
                        class_name="text-sm text-gray-500 mt-1",
                    ),
                    rx.el.button(
                        rx.icon("x", class_name="h-5 w-5"),
                        on_click=CallState.toggle_update_modal,
                        class_name="p-1 rounded-full hover:bg-gray-100 absolute top-4 right-4",
                    ),
                    class_name="pb-4 border-b relative",
                ),
                rx.el.div(
                    rx.el.input(
                        type="hidden",
                        name="id",
                        default_value=CallState.selected_call[
                            "id"
                        ].to_string(),
                    ),
                    rx.cond(
                        AuthState.is_admin,
                        rx.el.div(
                            rx.el.label(
                                "Assign To",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.select(
                                rx.foreach(
                                    CallState.agents,
                                    lambda agent: rx.el.option(
                                        agent, value=agent
                                    ),
                                ),
                                name="assigned_to",
                                default_value=CallState.selected_call[
                                    "assigned_to"
                                ],
                                class_name="w-full p-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500",
                            ),
                            class_name="space-y-1",
                        ),
                        rx.fragment(),
                    ),
                    rx.el.label(
                        "Status",
                        class_name="block text-sm font-medium text-gray-700 mt-4 mb-1",
                    ),
                    rx.el.select(
                        rx.el.option(
                            "Pending", value="Pending"
                        ),
                        rx.el.option(
                            "Completed", value="Completed"
                        ),
                        rx.el.option(
                            "Follow-up", value="Follow-up"
                        ),
                        name="status",
                        default_value=CallState.selected_call[
                            "status"
                        ],
                        class_name="w-full p-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500",
                    ),
                    rx.el.label(
                        "Remarks",
                        class_name="block text-sm font-medium text-gray-700 mt-4 mb-1",
                    ),
                    rx.el.textarea(
                        name="remarks",
                        default_value=CallState.selected_call[
                            "remarks"
                        ],
                        placeholder="Enter remarks...",
                        class_name="w-full p-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500",
                        rows=3,
                    ),
                    rx.el.label(
                        "Feedback",
                        class_name="block text-sm font-medium text-gray-700 mt-4 mb-1",
                    ),
                    rx.el.textarea(
                        name="feedback",
                        default_value=CallState.selected_call[
                            "feedback"
                        ],
                        placeholder="Enter customer feedback...",
                        class_name="w-full p-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500",
                        rows=3,
                    ),
                    class_name="py-4 space-y-2",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancel",
                        type="button",
                        on_click=CallState.toggle_update_modal,
                        class_name="px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 font-medium",
                    ),
                    rx.el.button(
                        "Save Changes",
                        type="submit",
                        class_name="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 font-medium",
                    ),
                    class_name="flex justify-end gap-3 pt-4 border-t",
                ),
                on_submit=CallState.update_call,
                reset_on_submit=True,
                class_name="bg-white p-6 rounded-xl shadow-lg w-full max-w-lg",
            ),
            rx.fragment(),
        ),
        open=CallState.show_update_modal,
        class_name="fixed inset-0 open:flex items-center justify-center bg-black/50 z-50",
    )