from datetime import datetime
from sqlalchemy.orm import Session
from tfl_client import fetch_arrivals
from models import engine, StopPoint, ArrivalObservation

arrivals = fetch_arrivals(["15"])
session = Session(engine)


for arrival in arrivals:
    existing_stop = session.get(StopPoint, arrival["naptanId"])
    if existing_stop is None:
        stop_point = StopPoint(
            naptanId=arrival["naptanId"],
            stationName=arrival["stationName"],
        )
        session.add(stop_point)

    timestamp = datetime.fromisoformat(
        arrival["timestamp"].replace("Z", "+00:00")
    )

    expected = datetime.fromisoformat(
        arrival["expectedArrival"].replace("Z", "+00:00")
    )

    observation = ArrivalObservation(
        lineId=arrival["lineId"],
        naptanId=arrival["naptanId"],
        vehicleId=arrival["vehicleId"],
        timestamp=timestamp,
        expectedArrival=expected,
        destinationName=arrival["destinationName"],
        timeToStation=arrival["timeToStation"]
    )

    session.add(observation)

session.commit()

print(f"Saved {len(arrivals)} observations")
print(f"Total observations: {session.query(ArrivalObservation).count()}")

stops = session.query(StopPoint).all()
