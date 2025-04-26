from nicegui import ui
from pages.layout import create_layout
import httpx

@ui.page("/manage_nodes")
async def manage_nodes():
    create_layout()
    ui.label('Manage a one of the existing edge nodes').classes('text-2xl')

    def open_node_manager(node_id: str):
        with ui.dialog() as dialog, ui.card().classes('w-200 h-200'):
            ui.label(f'Node: {node_id}')
            ui.input("Service_id")
            ui.input("device_id")
            ui.select(["PLC","Sensor"],label="Choose device type")
            ui.select(["Siemens","Other"], label="Choose manufacturer")
            ui.select(["S7-1200"],label="Choose model")
            ui.select(["Modbus TCP", "USB"],label="Choose communication protocol")
            ui.input("ip",value="127.0.0.1")
            ui.input("port",value=502)
            ui.input("Unit_id")
            datatypes = ui.select(["holding_register","coils"],multiple=True,label="Choose data types to extract")

            ui.button("Save", on_click=dialog.close)
        dialog.open()



    async def get_nodes_data():
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("http://localhost:8000/api/manage_nodes/get_nodes")
                data = response.json()

                return data

        except Exception as e:
            ui.notify(f"Failed to load the nodes: {e}", type="negative")

    node_data = await get_nodes_data()

    async def get_nodes_state():
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("http://localhost:8000/api/manage_nodes/get_node_state")
                data = response.json()

                return data

        except Exception as e:
            ui.notify(f"Failed to load the state of the nodes: {e}", type="negative")

    node_state = await get_nodes_state()

    with ui.row().classes("w-full"):
        with ui.column().classes("w-full grid grid-cols-3 gap-4"):
            for node in node_data:
                with ui.card().on("click", lambda _, n=node: open_node_manager(n["node_id"])) \
                        .classes("cursor-pointer hover:bg-blue-50 p-4"):
                    ui.label(f"Node: {node['node_id']}").classes("text-lg font-bold")
                    ui.label(f"Group: {node['group_id']}")
                    ui.label(f"IP: {node['ip']}")
                    state = "Online" if node_state[node["node_id"]]["state"] == "1" else "Offline"
                    ui.label(f'State: {state}')
