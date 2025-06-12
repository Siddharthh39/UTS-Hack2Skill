import reflex as rx
from typing import TypedDict, Any
import pandas as pd
import io
from collections import Counter
from call_management_system.states.auth_state import AuthState


class CallData(TypedDict):
    """Represents the structure of a call record."""
    id: int
    customer_name: str
    phone_number: str
    assigned_to: str
    status: str
    remarks: str
    feedback: str


class PieDataEntry(TypedDict):
    """Represents the structure of data for pie charts."""
    name: str
    value: int
    fill: str


class CallState(rx.State):
    """The state for managing calls in the application."""

    calls: list[CallData] = [
        {
            "id": 1,
            "customer_name": "John Doe",
            "phone_number": "123-456-7890",
            "assigned_to": "mayank.verma@hack2skill",
            "status": "Completed",
            "remarks": "Initial call",
            "feedback": "",
        },
        {
            "id": 2,
            "customer_name": "Jane Smith",
            "phone_number": "234-567-8901",
            "assigned_to": "priyanshu.singh@hack2skill",
            "status": "Completed",
            "remarks": "Resolved issue",
            "feedback": "Very helpful",
        },
        {
            "id": 3,
            "customer_name": "Peter Jones",
            "phone_number": "345-678-9012",
            "assigned_to": "satyam.kumar@hack2skill",
            "status": "Follow-up",
            "remarks": "Needs callback on Friday",
            "feedback": "",
        },
        {
            "id": 4,
            "customer_name": "Mary Johnson",
            "phone_number": "456-789-0123",
            "assigned_to": "",
            "status": "Pending",
            "remarks": "New lead",
            "feedback": "",
        },
        {
            "id": 5,
            "customer_name": "Chris Green",
            "phone_number": "567-890-1234",
            "assigned_to": "mayank.verma@hack2skill",
            "status": "Pending",
            "remarks": "Follow up needed",
            "feedback": "",
        },
        {
            "id": 6,
            "customer_name": "Lisa Ray",
            "phone_number": "678-901-2345",
            "assigned_to": "mayank.verma@hack2skill",
            "status": "Follow-up",
            "remarks": "Interested in product B",
            "feedback": "Good service",
        },
    ]
    agents: list[str] = [
        "mayank.verma@hack2skill",
        "priyanshu.singh@hack2skill",
        "satyam.kumar@hack2skill",
    ]
    search_query: str = ""
    show_upload_modal: bool = False
    show_update_modal: bool = False
    selected_call: CallData | None = None

    @rx.var
    async def filtered_calls(self) -> list[CallData]:
        """Returns the filtered list of calls based on the search query and user role."""
        auth_state = await self.get_state(AuthState)
        user_email = auth_state.logged_in_user_email
        role = await self.get_var_value(
            auth_state.get_current_user_role
        )
        if role == "admin":
            visible_calls = self.calls
        elif role == "agent":
            visible_calls = [
                call
                for call in self.calls
                if call["assigned_to"] == user_email
            ]
        else:
            visible_calls = []
        if not self.search_query:
            return visible_calls
        query = self.search_query.lower()
        return [
            call
            for call in visible_calls
            if query in call["customer_name"].lower()
            or query in call["phone_number"].lower()
            or query in call["assigned_to"].lower()
            or (query in call["status"].lower())
        ]

    @rx.var
    async def agent_call_status_pie_data(self) -> list[PieDataEntry]:
        """Generates pie chart data for the logged-in agent's call statuses."""
        auth_state = await self.get_state(AuthState)
        user_email = auth_state.logged_in_user_email
        user_calls = [
            call
            for call in self.calls
            if call["assigned_to"] == user_email
        ]
        if not user_calls:
            return []
        status_counts = Counter(
            (call["status"] for call in user_calls)
        )
        colors = {
            "Completed": "#22c55e",
            "Pending": "#f59e0b",
            "Follow-up": "#3b82f6",
        }
        return [
            {
                "name": status,
                "value": count,
                "fill": colors.get(status, "#6b7280"),
            }
            for status, count in status_counts.items()
        ]

    @rx.var
    def admin_call_status_pie_data(self) -> list[PieDataEntry]:
        """Generates pie chart data for all call statuses (admin view)."""
        if not self.calls:
            return []
        status_counts = Counter(
            (call["status"] for call in self.calls)
        )
        colors = {
            "Completed": "#22c55e",
            "Pending": "#f59e0b",
            "Follow-up": "#3b82f6",
        }
        return [
            {
                "name": status,
                "value": count,
                "fill": colors.get(status, "#6b7280"),
            }
            for status, count in status_counts.items()
        ]

    @rx.var
    def admin_overall_stats(self) -> dict[str, str | int]:
        """Calculates overall statistics for admin dashboard."""
        total_calls = len(self.calls)
        if not total_calls:
            return {
                "total_calls": 0,
                "unassigned": 0,
                "completed": 0,
                "max_status": "N/A",
            }
        unassigned = len(
            [c for c in self.calls if not c["assigned_to"]]
        )
        completed = len(
            [
                c
                for c in self.calls
                if c["status"] == "Completed"
            ]
        )
        status_counts = Counter(
            (call["status"] for call in self.calls)
        )
        max_status = (
            status_counts.most_common(1)[0][0]
            if status_counts
            else "N/A"
        )
        return {
            "total_calls": total_calls,
            "unassigned": unassigned,
            "completed": completed,
            "max_status": max_status,
        }

    @rx.var
    def admin_agent_stats(self) -> dict[str, dict[str, int]]:
        """Generates performance statistics for each agent."""
        stats: dict[str, dict[str, int]] = {}
        assigned_calls = [
            c for c in self.calls if c["assigned_to"]
        ]
        for agent in self.agents:
            agent_calls = [
                c
                for c in assigned_calls
                if c["assigned_to"] == agent
            ]
            completed = len(
                [
                    c
                    for c in agent_calls
                    if c["status"] == "Completed"
                ]
            )
            pending = len(agent_calls) - completed
            stats[agent] = {
                "completed": completed,
                "pending": pending,
                "total": len(agent_calls),
            }
        return stats

    @rx.event
    def toggle_upload_modal(self):
        """Toggles the visibility of the upload modal."""
        self.show_upload_modal = not self.show_upload_modal

    @rx.event
    def toggle_update_modal(self):
        """Toggles the visibility of the update modal."""
        self.show_update_modal = not self.show_update_modal
        if not self.show_update_modal:
            self.selected_call = None

    @rx.event
    def select_call_for_update(self, call: CallData):
        """Selects a call for updating and opens the update modal."""
        self.selected_call = call
        self.show_update_modal = True

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handles the upload of a CSV file containing call data."""
        if not files:
            yield rx.toast.error(
                "No files selected for upload."
            )
            return
        try:
            upload_data = await files[0].read()
            df = pd.read_csv(io.BytesIO(upload_data))
            required_columns = {
                "customer_name",
                "phone_number",
            }
            if not required_columns.issubset(df.columns):
                yield rx.toast.error(
                    f"CSV must contain columns: {', '.join(required_columns)}"
                )
                return
            new_calls = []
            max_id = (
                max([call["id"] for call in self.calls])
                if self.calls
                else 0
            )
            for _, row in df.iterrows():
                max_id += 1
                new_calls.append(
                    {
                        "id": max_id,
                        "customer_name": str(
                            row.get("customer_name", "")
                        ),
                        "phone_number": str(
                            row.get("phone_number", "")
                        ),
                        "assigned_to": str(
                            row.get("assigned_to", "")
                        ),
                        "status": str(
                            row.get("status", "Pending")
                        ),
                        "remarks": str(
                            row.get("remarks", "")
                        ),
                        "feedback": str(
                            row.get("feedback", "")
                        ),
                    }
                )
            self.calls.extend(new_calls)
            self.show_upload_modal = False
            yield rx.toast.success(
                f"Successfully uploaded and added {len(new_calls)} records."
            )
        except Exception as e:
            yield rx.toast.error(
                f"An error occurred during upload: {e}"
            )

    @rx.event
    def update_call(self, form_data: dict):
        """Updates the details of a selected call."""
        call_id = int(form_data.get("id", 0))
        if not call_id:
            return rx.toast.error("Invalid call ID.")
        for i, call in enumerate(self.calls):
            if call["id"] == call_id:
                self.calls[i]["status"] = form_data[
                    "status"
                ]
                self.calls[i]["remarks"] = form_data[
                    "remarks"
                ]
                self.calls[i]["feedback"] = form_data[
                    "feedback"
                ]
                if "assigned_to" in form_data:
                    self.calls[i]["assigned_to"] = (
                        form_data["assigned_to"]
                    )
                break
        self.show_update_modal = False
        self.selected_call = None
        return rx.toast.success(
            "Call updated successfully."
        )

    @rx.event
    def download_pivot_table(self):
        """Generates and downloads a pivot table of call data."""
        if not self.calls:
            return rx.toast.warning("No data to export.")
        df = pd.DataFrame(self.calls)
        df_assigned = df[df["assigned_to"] != ""]
        if df_assigned.empty:
            return rx.toast.warning(
                "No assigned calls to create a pivot table."
            )
        pivot = pd.pivot_table(
            df_assigned,
            values="id",
            index="assigned_to",
            columns="status",
            aggfunc="count",
            fill_value=0,
        )
        pivot["Total Assigned"] = pivot.sum(axis=1)
        csv_data = pivot.to_csv()
        return rx.download(
            data=csv_data, filename="uts_pivot_table.csv"
        )

    @rx.event
    def export_data(self):
        """Exports all call data to a CSV file."""
        if not self.calls:
            return rx.toast.warning("No data to export.")
        df = pd.DataFrame(self.calls)
        csv_data = df.to_csv(index=False)
        return rx.download(
            data=csv_data, filename="uts_call_data.csv"
        )