import reflex as rx
from call_management_system.states.call_state import CallState
from call_management_system.components.charts import pie_chart_component


def stat_card(
    title: str,
    value: rx.Var[str | int],
    icon: str,
    color: str,
) -> rx.Component:
    """A card for displaying a single statistic."""
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name=f"h-6 w-6 {color}"),
            class_name="p-3 bg-gray-100 rounded-lg",
        ),
        rx.el.div(
            rx.el.p(
                title,
                class_name="text-sm font-medium text-gray-500",
            ),
            rx.el.p(
                value,
                class_name="text-2xl font-bold text-gray-800",
            ),
            class_name="flex flex-col",
        ),
        class_name="flex items-center gap-4 bg-white p-4 rounded-xl border border-gray-200 shadow-sm",
    )


def agent_performance_card(
    agent: rx.Var[str],
) -> rx.Component:
    """A card for displaying an agent's performance."""
    agent_stats = CallState.admin_agent_stats.get(
        agent, {}
    ).to(dict)
    return rx.el.div(
        rx.el.div(
            rx.el.img(
                src=f"https://api.dicebear.com/9.x/initials/svg?seed={agent}",
                class_name="h-12 w-12 rounded-full",
            ),
            rx.el.div(
                rx.el.p(
                    agent,
                    class_name="font-semibold text-gray-800",
                ),
                rx.el.p(
                    f"{agent_stats.get('total', 0).to_string()} Calls Assigned",
                    class_name="text-sm text-gray-500",
                ),
                class_name="flex-grow",
            ),
            class_name="flex items-center gap-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Completed",
                    class_name="text-xs text-gray-500",
                ),
                rx.el.p(
                    agent_stats.get(
                        "completed", 0
                    ).to_string(),
                    class_name="text-lg font-bold text-green-600",
                ),
                class_name="text-center",
            ),
            rx.el.div(
                rx.el.p(
                    "Pending",
                    class_name="text-xs text-gray-500",
                ),
                rx.el.p(
                    agent_stats.get(
                        "pending", 0
                    ).to_string(),
                    class_name="text-lg font-bold text-yellow-600",
                ),
                class_name="text-center",
            ),
            class_name="flex gap-6",
        ),
        class_name="flex items-center justify-between bg-white p-4 rounded-xl border border-gray-200 shadow-sm",
    )


def admin_dashboard() -> rx.Component:
    """The admin dashboard component showing call statistics."""
    return rx.el.div(
        rx.el.h2(
            "Admin Dashboard",
            class_name="text-2xl font-bold text-gray-800",
        ),
        rx.el.p(
            "Overall performance and call distribution.",
            class_name="text-gray-500 mb-6",
        ),
        rx.el.div(
            stat_card(
                "Total Calls",
                CallState.admin_overall_stats.get(
                    "total_calls", 0
                ).to_string(),
                "phone",
                "text-blue-500",
            ),
            stat_card(
                "Completed Calls",
                CallState.admin_overall_stats.get(
                    "completed", 0
                ).to_string(),
                "check_check",
                "text-green-500",
            ),
            stat_card(
                "Unassigned Calls",
                CallState.admin_overall_stats.get(
                    "unassigned", 0
                ).to_string(),
                "user-plus",
                "text-yellow-500",
            ),
            stat_card(
                "Top Status",
                CallState.admin_overall_stats.get(
                    "max_status", "N/A"
                ).to_string(),
                "trending-up",
                "text-purple-500",
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8",
        ),
        rx.el.div(
            pie_chart_component(
                data=CallState.admin_call_status_pie_data,
                title="Overall Call Status Distribution",
            ),
            rx.el.div(
                rx.el.h3(
                    "Agent Performance",
                    class_name="text-lg font-bold text-gray-800 mb-4",
                ),
                rx.el.div(
                    rx.foreach(
                        CallState.agents,
                        agent_performance_card,
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
                ),
                class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm",
            ),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8",
        ),
    )