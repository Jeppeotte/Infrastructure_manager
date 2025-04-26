from nicegui import ui
import httpx
from pages.layout import create_layout


@ui.page("/")
async def dashboard():
    create_layout()
    ui.label('Dashboard').classes('text-2xl')
    # Create containers for the data
    status_label = ui.label("Loading status...")
    node_count_label = ui.label("Loading node count...")
    last_updated_label = ui.label("")

    async def load_data():
        """Fetch and display data automatically"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("http://localhost:8000/api/dashboard/status")
                data = response.json()

                # Update UI elements
                status_label.text = f"System status: {data['status'].upper()}"
                node_count_label.text = f"Active nodes: {data['node_count']}"
                last_updated_label.text = f"Last updated: {data['last_updated']}"

                # Visual feedback
                if data['status'] == "online":
                    status_label.classes(replace="text-positive")
                else:
                    status_label.classes(replace="text-negative")

        except Exception as e:
            ui.notify(f"Failed to load data: {e}", type="negative")
            status_label.text = "Error loading data"
            status_label.classes(replace="text-negative")

    await load_data()

    ui.button("Refresh", on_click=load_data)