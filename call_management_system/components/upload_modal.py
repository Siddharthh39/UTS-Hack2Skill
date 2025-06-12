import reflex as rx
from call_management_system.states.call_state import CallState

upload_id = "csv_upload_area"


def upload_modal() -> rx.Component:
    """Renders the CSV upload modal."""
    return rx.el.dialog(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Upload CSV File",
                    class_name="text-lg font-semibold text-gray-800",
                ),
                rx.el.button(
                    rx.icon("x", class_name="h-5 w-5"),
                    on_click=CallState.toggle_upload_modal,
                    class_name="p-1 rounded-full hover:bg-gray-100",
                ),
                class_name="flex justify-between items-center pb-4 border-b",
            ),
            rx.el.div(
                rx.upload.root(
                    rx.el.div(
                        rx.icon(
                            "cloud-upload",
                            class_name="w-10 h-10 text-gray-400 mb-3",
                        ),
                        rx.el.p(
                            "Drag & drop files here, or click to select files",
                            class_name="text-sm text-gray-600",
                        ),
                        class_name="flex flex-col items-center justify-center p-10 border-2 border-dashed border-gray-300 rounded-lg bg-gray-50 cursor-pointer hover:bg-gray-100",
                    ),
                    id=upload_id,
                    accept={"text/csv": [".csv"]},
                    multiple=False,
                    max_files=1,
                    class_name="w-full my-5",
                ),
                rx.el.div(
                    rx.foreach(
                        rx.selected_files(upload_id),
                        lambda file: rx.el.div(
                            rx.icon(
                                "file-text",
                                class_name="h-5 w-5 text-indigo-600",
                            ),
                            rx.el.span(
                                file,
                                class_name="text-sm font-medium",
                            ),
                            class_name="flex items-center gap-2 p-2 bg-indigo-50 rounded-md border border-indigo-200",
                        ),
                    ),
                    class_name="space-y-2",
                ),
                class_name="py-4",
            ),
            rx.el.div(
                rx.el.button(
                    "Cancel",
                    on_click=CallState.toggle_upload_modal,
                    class_name="px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 font-medium",
                ),
                rx.el.button(
                    "Upload",
                    on_click=CallState.handle_upload(
                        rx.upload_files(upload_id=upload_id)
                    ),
                    class_name="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 font-medium",
                ),
                class_name="flex justify-end gap-3 pt-4 border-t",
            ),
            class_name="bg-white p-6 rounded-xl shadow-lg w-full max-w-lg",
        ),
        open=CallState.show_upload_modal,
        class_name="fixed inset-0 open:flex items-center justify-center bg-black/50 z-50",
    )