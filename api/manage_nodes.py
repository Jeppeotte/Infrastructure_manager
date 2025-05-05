from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from db.db_session import get_postgres_db
from db.db_operations import get_all_nodes, get_latest_node_state, get_specific_node
from pydantic import BaseModel
from pathlib import Path
from ruamel.yaml import YAML
import subprocess
import sys
from models.config_models import  S7CommDeviceServiceConfig

class Device(BaseModel):
    group_id: str
    node_id: str
    device_id: str
    alias: str | None = None
    manufacturer: str
    model: str
    protocol_type: str
    ip: str
    port: int
    unit_id: int | None = None
    rack: int | None = None
    slot: int | None = None

class PollingInterval(BaseModel):
    default_coil_interval: float
    default_register_interval: float

class HoldingRegisters(BaseModel):
    name: str
    address: int
    data_type: str
    units: str

class Coils(BaseModel):
    name: str
    address: int

class ModbusDeviceServiceConfig(BaseModel):
    device: Device
    polling: PollingInterval
    holding_registers: list[HoldingRegisters] | None=None
    coils: list[Coils] | None=None

class DeviceServiceTestParameters(BaseModel):
    configfile_path: str



router = APIRouter(prefix="/api/manage_nodes")

@router.get("/get_all_nodes")
async def get_all_nodes_info(db: Session = Depends(get_postgres_db)):
    #Get all nodes from the database

    return get_all_nodes(db)

@router.get("/get_node_state")
async def get_node_state(db: Session = Depends(get_postgres_db)):
    # Get the latest state of the nodes
    return get_latest_node_state(db)

@router.post("/configure_device_service")
async def configure_device_service(config: ModbusDeviceServiceConfig):
    # Creates a config file for the service within the right folder
    try:
        config_directory = Path.cwd().joinpath(f"devices/configs/{config.device.protocol_type}")

        config_directory.mkdir(parents=True,exist_ok=True)

        configfile_path = config_directory.joinpath(f"{config.device.device_id}.yaml")

        yaml = YAML()
        yaml.preserve_quotes = True
        yaml.indent(mapping=2, sequence=4, offset=2)


        with open(configfile_path,'w') as f:
            yaml.dump(config.model_dump(),f)

        return {"configfile_path": configfile_path}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def run_modbus_tester(configfile_path: str):
    #Tests the modbus device service
    tester_path = Path.cwd().joinpath("modbus_tcp_tester.py")
    result = subprocess.run([sys.executable, tester_path, "--configfile_path", configfile_path],
                   capture_output=True, text=True)
    return result.stdout

@router.post("/test_device_service")
async def test_device_service(params: DeviceServiceTestParameters):
    # Test the device service and modify the metadata
    try:
        result = run_modbus_tester(params.configfile_path)
        return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/activate_device_service")
async def activate_device_service():
    #After the device service has been added it has to be activated/started
    #Activating the device service through spinning up the container or script

    return

@router.get("/{node_id}")
async def get_node_details(node_id: str, db: Session = Depends(get_postgres_db)):
    #Get the information about the specific node which want to be managed
    return get_specific_node(node_id,db)

@router.post("/add_S7_device") # API for edge node
async def add_S7_device(serviceconfig: S7CommDeviceServiceConfig):
    #Create the config file for the device service
    try:
        # Define the directory for the device service
        core_path = Path.cwd().joinpath(f"devices/{serviceconfig.device.protocol_type}")
        # Check if path exist and create it if not:
        # Create file path if it does not exist
        core_path.mkdir(parents=True, exist_ok=True)
        # Define the file path for metadata.yaml
        configfile_path = core_path.joinpath(f"{serviceconfig.device.device_id}.yaml")

        yaml = YAML()
        yaml.preserve_quotes = True
        yaml.indent(mapping=2, sequence=4, offset=2)

        with open(configfile_path, 'w') as f:
            yaml.dump(serviceconfig.model_dump(), f)

        return {"configfile_path": configfile_path}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

