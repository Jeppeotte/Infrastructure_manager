from pydantic import BaseModel


# General models
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

class DeviceServiceTestParameters(BaseModel):
    configfile_path: str

class PollingInterval(BaseModel):
    default_interval: float
    trigger_interval: float
    data_interval: float

# Modbus specific models
class ModbusPollingInterval(BaseModel):
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
    polling: ModbusPollingInterval
    holding_registers: list[HoldingRegisters] | None = None
    coils: list[Coils] | None = None

#S7comm specific models
class S7commTrigger(BaseModel):
    name: str
    description: str | None = None
    db_number: int
    read_size: int
    data_type: str
    byte_offset: int
    bit_offset: int
    units: str | None = None
    condition: bool

class S7commVariables(BaseModel):
    name: str
    data_type:str
    byte_offset: int
    bit_offset: int
    units: str

class DataBlock(BaseModel):
    name: str
    db_number: int
    read_size: int
    byte_offset: int
    variables: list[S7commVariables]

class S7CommDeviceServiceConfig(BaseModel):
    device: Device
    polling: PollingInterval
    trigger: S7commTrigger
    data_block: DataBlock

