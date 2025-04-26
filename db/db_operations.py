from importlib.metadata import metadata

from sqlalchemy.orm import Session
from sqlalchemy import inspect, select, MetaData, Table, desc, null
from models.add_nodes import EdgeNode, Base, NodeConfig
from fastapi import HTTPException, status
from db.db_session import engine

def create_edge_node(db: Session, node_data: NodeConfig):
    #Check if the table "edge_nodes" exist
    inspector = inspect(db.get_bind())
    if "edge_nodes" not in inspector.get_table_names():
        #If the table do not exist, create the table
        Base.metadata.create_all(bind=engine, tables=[EdgeNode.__table__])
        db.commit()

    # Check for duplicate node_id
    if db.query(EdgeNode).filter(EdgeNode.node_id == node_data.node_id).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Node ID {node_data.node_id} already exists"
        )

    try:
        # Prepare data
        db_node = EdgeNode(
            node_id=node_data.node_id,
            group_id=node_data.group_id,
            ip=node_data.ip,
            description=node_data.description,
            app_services=node_data.app_services
        )
        db.add(db_node)
        db.commit()
        db.refresh(db_node)
        return db_node

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

def get_all_nodes(db: Session):
    # Get all nodes from "edge_nodes" database for configuration
    session = Session(engine)
    # Select statement - Selecting the Edgenode model
    stmt = select(EdgeNode)

    return list(session.scalars(stmt))

def get_latest_node_state(db: Session):
    metadata = MetaData()
    result = {}

    #Get all unique group_ids from edge_nodes
    group_ids = db.scalars(select(EdgeNode.group_id).distinct()).all()

    for group_id in group_ids:
        # get table metadata (group_id and columns)
        group_table = Table(group_id, metadata, autoload_with=db.bind)

        # Create query to get the latest state for each edge_node_id where device_id is null
        stmt = (
            select(
                group_table.c.edge_node_id,
                group_table.c.time,
                group_table.c.state
            )
            .where(group_table.c.device_id == "null")  # Ensure device_id is NULL
            .distinct(group_table.c.edge_node_id)  # Get the latest for each edge_node_id
            .order_by(group_table.c.edge_node_id, group_table.c.time.desc())  # Order by edge_node_id and time DESC
        )

        latest_rows = db.execute(stmt).fetchall()  # Execute the query and fetch all rows

        for node_id, time, state in latest_rows:
            result[node_id] = {"time": time.timestamp(), "state": state}

    return result
