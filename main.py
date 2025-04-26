from fastapi import FastAPI
from nicegui import ui
import uvicorn

# Initialize FastAPI
app = FastAPI()

# Import all API routers
from api.dashboard import router as dashboard_router
from api.add_nodes import router as add_nodes_router
from api.manage_nodes import router as manage_nodes_router

app.include_router(dashboard_router)
app.include_router(add_nodes_router)
app.include_router(manage_nodes_router)

# Import all pages
from pages import dashboard, add_nodes, manage_nodes

# -----------------------------------------------------------------------------
# Run Both FastAPI and NiceGUI Together
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    ui.run_with(
        app,
        mount_path="/",
        title="Edge Node Manager"
    )
    uvicorn.run(app, host="0.0.0.0", port=8000)
