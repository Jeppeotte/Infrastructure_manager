from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import ARRAY
from db.db_session import Base
from pydantic import BaseModel

# Define the structure for configuring the edge node
class NodeConfig(BaseModel):
    group_id: str
    node_id: str
    description: str | None = None
    ip: str
    app_services: list[str] = []

#Database class for the edge nodes
class EdgeNode(Base):
    __tablename__ = "edge_nodes"

    node_id = Column(String, primary_key=True, index=True)
    group_id = Column(String)
    description = Column(String)
    ip = Column(String)
    app_services = Column(ARRAY(String))
    device_services = Column(ARRAY(String), nullable=True)