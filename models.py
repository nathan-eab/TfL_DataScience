from sqlalchemy import Column, DateTime, Integer, String, Float, create_engine
from sqlalchemy.orm import declarative_base

engine = create_engine("sqlite:///tfl_data.db")
Base = declarative_base()

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

class ArrivalObservation(Base):
    __tablename__ = "arrival_observations"
    id = Column(Integer, primary_key=True)
    lineId = Column(String)
    naptanId = Column(String)
    timestamp = Column(DateTime)
    expectedArrival = Column(DateTime)
    destinationName = Column(String)
    timeToStation = Column(Integer)
    vehicleId = Column(String)

Base.metadata.create_all(engine)



"""
notes:
- Naming conventions for classes i.e PascalCase and for variables snake_case. 
"""