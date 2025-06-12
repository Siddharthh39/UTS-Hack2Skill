import reflex as rx
from call_management_system.components.charts import pie_chart_component
from call_management_system.components.call_table import call_table
from call_management_system.states.call_state import CallState


def user_dashboard() -> rx.Component:
    """The user dashboard, showing their stats and assigned calls."""
    return rx.el.div(
        pie_chart_component(
            data=CallState.agent_call_status_pie_data,
            title="Your Call Status Overview",
        ),
        rx.el.div(call_table(), class_name="mt-8"),
    )