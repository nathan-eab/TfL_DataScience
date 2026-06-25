from sqlalchemy import Column, String, Float
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
import tfl_client

arrivals = tfl_client.fetch_arrivals(["15"])

engine = create_engine("sqlite:///tfl_data.db")
Base = declarative_base()
session = Session(engine)

class Line(Base):
    __tablename__ = "lines"
    lineId = Column(String, primary_key=True)
    line_name = Column(String)

class StopPoint(Base):
    __tablename__ = "stop_points"
    naptanId = Column(String, primary_key=True)
    stationName = Column(String)
    lat = Column(Float)
    lon = Column(Float)

Base.metadata.create_all(engine)


for arrival in arrivals:
    existing_stop = session.get(StopPoint, arrival["naptanId"])
    if existing_stop is None:
        stop_point = StopPoint(
            naptanId=arrival["naptanId"],
            stationName=arrival["stationName"],
        )
        session.add(stop_point)

session.commit()

stops = session.query(StopPoint).all()
print(len(stops))

for stop in stops[:10]:
    print(stop.naptanId, "-", stop.stationName)

"""
notes:
- Naming conventions for classes i.e PascalCase and for variables snake_case. 
"""