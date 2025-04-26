from nicegui import ui

# Create the shared layout.
def create_layout():
    with ui.header(elevated=True).style('background-color: #3874c8'):
        ui.label('EDGE NODE MANAGER').classes('text-white text-xl')

    with ui.left_drawer(bottom_corner=True).style('background-color: #e8f4ff'):
        ui.button('Dashboard', on_click=lambda: ui.navigate.to('/'))
        ui.button('Add Node', on_click=lambda: ui.navigate.to('/add_node'))
        ui.button('Manage Nodes', on_click=lambda: ui.navigate.to('/manage_nodes'))