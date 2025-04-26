from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from db.db_session import get_db
from db.db_operations import get_all_nodes, get_latest_node_state
from pydantic import BaseModel
from pathlib import Path
from ruamel.yaml import YAML
import subprocess
import sys

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
    unit_id: int

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

@router.get("/get_nodes")
async def get_nodes(db: Session = Depends(get_db)):
    #Get all nodes from the database
    return get_all_nodes(db)

@router.get("/get_node_state")
async def get_node_state(db: Session = Depends(get_db)):
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




def run_modbustester(configfile_path: str):
    tester_path = Path.cwd().joinpath("modbus_tcp_tester.py")
    result = subprocess.run([sys.executable, tester_path, "--configfile_path", configfile_path],
                   capture_output=True, text=True)
    return result.stdout

@router.post("/test_device_service")
async def test_device_service(params: DeviceServiceTestParameters):
    # Test the device service and modify the metadata
    try:
        result = run_modbustester(params.configfile_path)
        return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/activate_device_service")
async def activate_device_service():
    #If the device service is not active, activate it

    #Create the config file for the modbus_tcp service

    #Test connection

    # Edit metadata file

    return

