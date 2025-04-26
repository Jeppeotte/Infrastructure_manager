from nicegui import ui
from pages.layout import create_layout
import httpx
import json


@ui.page("/add_node")
def add_node_page():
    create_layout()
    ui.label('Add a new edge node').classes('text-2xl')

    # Form elements
    node_id = ui.input("Node ID")
    group_id = ui.input("Group ID")
    description = ui.input("Description")
    node_ip = ui.input("Node IP address")
    ui.label('Connections:')

    connections = []
    def toggle_mqtt(e):
        if e.value:  # Checkbox checked
            if 'MQTT' not in connections:
                connections.append('MQTT')
        else:  # Checkbox unchecked
            if 'MQTT' in connections:
                connections.remove('MQTT')

    ui.checkbox('MQTT', on_change=toggle_mqtt)



    async def add_node():
        # Add the node to the system and configure it
        node_data = {"group_id": group_id.value,
                     "node_id": node_id.value,
                     "description": description.value,
                     "ip": node_ip.value,
                     "app_services": connections,
                     "device_services": []
                     }

        ui.notify(json.dumps(node_data))
        try:
            async with httpx.AsyncClient() as client:
                # First configure the node
                api_url = f"http://localhost:8000/api/add_nodes/configure_node"
                node_response = await client.post(api_url, json=node_data)

                if node_response.status_code != 200:
                    ui.notify(f"Failed to configure node, status code: {node_response.status_code}", type="negative")
                    return

                # Second add to db
                database_response = await client.post("http://localhost:8000/api/add_nodes/create_node",
                                                      json=node_data)

                if database_response.status_code != 200:
                    ui.notify(f"Failed to create node in db, status code: {database_response.status_code}",
                              type="negative")
                    return

                ui.notify("Node successfully configured and added")


        except Exception as e:
            ui.notify(f"Failed during node setup: {e}", type="negative")

    # Add node
    ui.button("Add node", on_click=add_node)