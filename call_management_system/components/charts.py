import reflex as rx
from typing import TypedDict


class PieDataEntry(TypedDict):
    name: str
    value: int
    fill: str


def pie_legend_item(item: dict) -> rx.Component:
    """Renders a single item for the pie chart legend."""
    return rx.el.div(
        rx.el.span(
            class_name="w-3 h-3 inline-block mr-2 rounded-sm",
            style={"backgroundColor": item["fill"]},
        ),
        rx.el.span(
            item["name"] + ": " + item["value"].to_string(),
            class_name="text-sm text-gray-600 font-medium",
        ),
        class_name="flex items-center",
    )


def pie_chart_component(
    data: rx.Var[list[PieDataEntry]], title: str
) -> rx.Component:
    """Creates a pie chart component with a custom HTML legend."""
    return rx.el.div(
        rx.el.h3(
            title,
            class_name="text-lg font-semibold text-gray-800 mb-4",
        ),
        rx.cond(
            data.length() > 0,
            rx.el.div(
                rx.recharts.pie_chart(
                    rx.recharts.graphing_tooltip(
                        cursor={
                            "fill": "rgba(200, 200, 200, 0.1)"
                        }
                    ),
                    rx.recharts.pie(
                        data=data,
                        data_key="value",
                        name_key="name",
                        cx="50%",
                        cy="50%",
                        inner_radius="50%",
                        outer_radius="80%",
                        padding_angle=5,
                        label=False,
                    ),
                    width="100%",
                    height=250,
                ),
                rx.el.div(
                    rx.foreach(data, pie_legend_item),
                    class_name="grid grid-cols-2 md:grid-cols-3 gap-x-4 gap-y-2 mt-4",
                ),
                class_name="relative flex flex-col items-center",
            ),
            rx.el.div(
                rx.el.p("No data available to display."),
                class_name="flex items-center justify-center h-[300px] text-gray-500 bg-gray-50 rounded-lg",
            ),
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm",
    )