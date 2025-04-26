from sqlalchemy.orm import Session
from sqlalchemy import inspect, select, MetaData, Table, desc, null
from models.add_nodes import EdgeNode, Base, NodeConfig
from fastapi import HTTPException, status
from db.db_session import engine, get_db


db = Session(engine)

def get_latest_node_state():
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

if __name__ == "__main__":

    print(get_latest_node_state())