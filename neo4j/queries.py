query_test = """
        MATCH (accident:Accident)-[:INVOLVES]->(vehicle:Vehicle)-[:HAS_VEHICLE_TYPE]->(vehicleType:VehicleType {type: 'Car'})
        MATCH (accident)-[:DATE_WAS]->(date:Date)
        WHERE substring(date.date, 0, 4) = '2016'
        MATCH (vehicle)-[:MADE_BY]->(make:Make {name: 'LAMBORGHINI'})
        MATCH (vehicle)-[:MODEL]->(model:Model)
        RETURN accident, date, vehicle, make, model
        LIMIT 100
        """


def get_all_car_accidents_by_make_and_accident_year(make, year):
    query = """
        MATCH (accident:Accident)-[:INVOLVES]->(vehicle:Vehicle)-[:HAS_VEHICLE_TYPE]->(vehicleType:VehicleType {type: 'Car'})
        MATCH (accident)-[:DATE_WAS]->(date:Date)
        WHERE substring(date.date, 0, 4) = $year
        MATCH (vehicle)-[:MADE_BY]->(make:Make {name: $make})
        MATCH (vehicle)-[:MODEL]->(model:Model)
        RETURN accident, date, vehicle, make, model
        LIMIT 100
        """
    parameters = {"make": make, "year": year}
    return query, parameters


def get_longitude_and_latitude_for_all_car_accidents_by_year(year, limit=1000):
    query = """
        MATCH (accident:Accident)-[:INVOLVES]->(vehicle:Vehicle)-[:HAS_VEHICLE_TYPE]->(vehicleType:VehicleType {type: 'Car'})
        MATCH (accident)-[:DATE_WAS]->(date:Date)
        WHERE substring(date.date, 0, 4) = $year
        MATCH (vehicle)-[:MADE_BY]->(make:Make)
        RETURN  accident.index, accident.latitude, accident.longitude
        LIMIT $limit
        """
    parameters = {"year": year, "limit": limit}
    return query, parameters


def get_accident_by_index(index):
    query = """
        MATCH (accident:Accident {index: $index})-[:INVOLVES]->(vehicle:Vehicle)-[:HAS_VEHICLE_TYPE]->(vehicleType:VehicleType)
        MATCH (accident)-[:DATE_WAS]->(date:Date)
        MATCH (vehicle)-[:MADE_BY]->(make:Make)
        RETURN accident, vehicle, vehicleType, make, date
        """
    parameters = {"index": index}
    return query, parameters