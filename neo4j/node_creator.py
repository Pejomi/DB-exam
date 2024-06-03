import numpy as np

def create_nodes(df, conn, chunk_size):
    query = """
    UNWIND $rows as row

    // Accident node
    MERGE (accident:Accident {
        index: row.Accident_Index
    })
    ON CREATE SET
        accident.latitude = toFloat(row.Latitude),
        accident.longitude = toFloat(row.Longitude),
        accident.time = row.Time,
        accident.number_of_vehicles = toInteger(row.Number_of_Vehicles),
        accident.casualties = toInteger(row.Number_of_Casualties)

    // Severity node
    MERGE (severity:Severity {level: row.Accident_Severity})
    MERGE (accident)-[:HAS_SEVERITY]->(severity)

    // Date node
    MERGE (date:Date {date: row.Date})
    MERGE (accident)-[:DATE_WAS]->(date)

    // Speed limit node
    MERGE (speedLimit:SpeedLimit {limit: toInteger(row.Speed_limit)})
    MERGE (accident)-[:HAS_SPEED_LIMIT]->(speedLimit)
    
    // Road type node
    MERGE (roadType:RoadType {type: row.Road_Type})
    MERGE (accident)-[:ROAD_TYPE_WAS]->(roadType)

    // Weather conditions node
    MERGE (weather:Weather {condition: row.Weather_Conditions})
    MERGE (accident)-[:WEATHER_WAS]->(weather)

    // Light conditions node
    MERGE (light:Light {condition: row.Light_Conditions})
    MERGE (accident)-[:LIGHT_WAS]->(light)

    // Road surface conditions node
    MERGE (roadSurface:RoadSurface {condition: row.Road_Surface_Conditions})
    MERGE (accident)-[:ROAD_SURFACE_WAS]->(roadSurface)

    // 1st point of impact node
    MERGE (pointOfImpact:PointOfImpact {impact: row['X1st_Point_of_Impact']})
    MERGE (accident)-[:IMPACTED_FIRST]->(pointOfImpact)

    // Urban or rural area node
    MERGE (accidentArea:Area {area: row.Urban_or_Rural_Area})
    MERGE (accident)-[:ACCIDENT_AREA_WAS]->(accidentArea)

    // Vehicle Manoeuvre node
    MERGE (manoeuvre:Manoeuvre {type: row.Vehicle_Manoeuvre})
    MERGE (accident)-[:VEHICLE_MANOEUVRE]->(manoeuvre)

    // ========================================================
    
    // Vehicle node 
    MERGE (vehicle:Vehicle {id: row.make + '_' + row.Accident_Index})
    ON CREATE SET
        vehicle.age = toInteger(row.Age_of_Vehicle),
        vehicle.hit_object_in_carriageway = row.Hit_Object_in_Carriageway,
        vehicle.hit_object_off_carriageway = row.Hit_Object_off_Carriageway
    MERGE (accident)-[:INVOLVES]->(vehicle)
    
    // Vehicle type node
    MERGE (vehicleType:VehicleType {type: row.Vehicle_Type})
    MERGE (vehicle)-[:HAS_VEHICLE_TYPE]->(vehicleType)
    
    // Make node
    MERGE (make:Make {name: row.make})
    MERGE (vehicle)-[:MADE_BY]->(make)

    // Model node
    MERGE (model:Model {name: row.model})
    MERGE (vehicle)-[:MODEL]->(model)

    // ========================================================

    // Driver node
    MERGE (driver:Driver {id: row.model + ' ' + row.Accident_Index + '_' + row.Sex_of_Driver})
    MERGE (vehicle)-[:DRIVEN_BY]->(driver)

    // Sex node
    MERGE (sex:Sex {type: row.Sex_of_Driver})
    MERGE (driver)-[:HAS_SEX]->(sex)

    // Age band node
    MERGE (ageBand:AgeBand {band: row.Age_Band_of_Driver})
    MERGE (driver)-[:HAS_AGE_BAND]->(ageBand)

    // Driver home area node
    MERGE (driverArea:Area {area: row.Driver_Home_Area_Type})
    MERGE (driver)-[:LIVES_IN]->(driverArea)
    
    """
    total_rows = len(df)
    number_of_chunks = (total_rows + chunk_size - 1) // chunk_size
    for i, chunk in enumerate(np.array_split(df, number_of_chunks)):
        parameters = {"rows": chunk.to_dict('records')}
        conn.execute_query(query, parameters)
        print(f"Processed batch {i + 1}/{number_of_chunks}, approximately {100 * (i + 1) / number_of_chunks:.2f}% complete")
