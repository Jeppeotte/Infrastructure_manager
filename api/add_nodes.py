from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from models.add_nodes import NodeConfig
from db.db_session import get_db
from db.db_operations import create_edge_node
from ruamel.yaml import YAML
from pathlib import Path

router = APIRouter(prefix="/api/add_nodes")


@router.get("/configurations")
async def get_configurations():
    #Get possible configuration such as already existing group IDs

    return None

@router.post("/create_node")
async def create_node(config: NodeConfig, db: Session = Depends(get_db)):
    #Connect to the db and insert the node information

    try:
        # Your CRUD logic uses 'db' internally
        new_node = create_edge_node(db, config)
        return {"status": "success", "node_id": new_node.node_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/configure_node")
async def configure_node(config: NodeConfig):
    try:
        # Define the core directory path for metadata.yaml
        core_path = Path.cwd().joinpath("core")
        # Check if path exist and create it if not:
        # Create the metadata file if it does not exsist
        core_path.mkdir(parents=True, exist_ok=True)
        # Define the file path for metadata.yaml
        metadata_path = core_path.joinpath("metadata.yaml")

        # Load existing YAML
        yaml = YAML()
        yaml.preserve_quotes = True
        yaml.indent(mapping=2, sequence=4, offset=2)

        if not metadata_path.exists():
            raise HTTPException(status_code=500, detail="metadata.yaml does not exist")

        with open(metadata_path, 'r') as f:
            metadata = yaml.load(f)

        # Update identity
        metadata["identity"]["group_id"] = config.group_id
        metadata["identity"]["node_id"] = config.node_id
        metadata["identity"]["description"] = config.description
        metadata["identity"]["ip"] = config.ip

        # Enable application services based on connections
        for service in config.app_services:
            service_key = service.lower() + "_publisher"  # e.g. "MQTT" → "mqtt_publisher"
            app_services = metadata["services"]["application_services"]

            if service_key in app_services:
                app_services[service_key]["enabled"] = True
            else:
                raise HTTPException(status_code=400, detail=f"Service '{service_key}' not found in metadata.")

        # Save updated YAML back to file
        with open(metadata_path, 'w') as f:
            yaml.dump(metadata, f)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return

