from neo4j import GraphDatabase

class Neo4jConnection:
    def __init__(self, uri, user, pwd):
        self._driver = GraphDatabase.driver(uri, auth=(user, pwd))

    def close(self):
        self._driver.close()

    def execute_query(self, query, parameters=None):
        with self._driver.session() as session:
            with session.begin_transaction() as tx:
                tx.run(query, parameters)

    def execute_read_query(self, query, parameters=None):
        with self._driver.session() as session:
            with session.begin_transaction() as tx:
                result = tx.run(query, parameters)
                return result.data()


    def create_indexes(self):
        index_queries = [
            # Accident node
            "CREATE CONSTRAINT FOR (accident:Accident) REQUIRE accident.index IS UNIQUE",
            "CREATE INDEX FOR (accident:Accident) ON (accident.latitude)",
            "CREATE INDEX FOR (accident:Accident) ON (accident.longitude)",
            "CREATE INDEX FOR (accident:Accident) ON (accident.time)",
            "CREATE INDEX FOR (accident:Accident) ON (accident.number_of_vehicles)",
            "CREATE INDEX FOR (accident:Accident) ON (accident.casualties)",

            # Severity node
            "CREATE INDEX FOR (severity:Severity) ON (severity.level)",

            # Date node
            "CREATE INDEX FOR (date:Date) ON (date.date)",

            # SpeedLimit node
            "CREATE INDEX FOR (speedLimit:SpeedLimit) ON (speedLimit.limit)",

            # RoadType node
            "CREATE INDEX FOR (roadType:RoadType) ON (roadType.type)",

            # Weather node
            "CREATE INDEX FOR (weather:Weather) ON (weather.condition)",

            # Light node
            "CREATE INDEX FOR (light:Light) ON (light.condition)",

            # RoadSurface node
            "CREATE INDEX FOR (roadSurface:RoadSurface) ON (roadSurface.condition)",

            # PointOfImpact node
            "CREATE INDEX FOR (pointOfImpact:PointOfImpact) ON (pointOfImpact.impact)",

            # Area node
            "CREATE INDEX FOR (area:Area) ON (area.area)",

            # Manoeuvre node
            "CREATE INDEX FOR (manoeuvre:Manoeuvre) ON (manoeuvre.type)",

            # Vehicle node
            "CREATE CONSTRAINT FOR (vehicle:Vehicle) REQUIRE vehicle.id IS UNIQUE",
            "CREATE INDEX FOR (vehicle:Vehicle) ON (vehicle.age)",
            "CREATE INDEX FOR (vehicle:Vehicle) ON (vehicle.hit_object_in_carriageway)",
            "CREATE INDEX FOR (vehicle:Vehicle) ON (vehicle.hit_object_off_carriageway)",

            # VehicleType node
            "CREATE INDEX FOR (vehicleType:VehicleType) ON (vehicleType.type)",

            # Make node
            "CREATE INDEX FOR (make:Make) ON (make.name)",

            # Model node
            "CREATE INDEX FOR (model:Model) ON (model.name)",

            # Driver node
            "CREATE CONSTRAINT FOR (driver:Driver) REQUIRE driver.id IS UNIQUE",

            # Sex node
            "CREATE INDEX FOR (sex:Sex) ON (sex.type)",

            # AgeBand node
            "CREATE INDEX FOR (ageBand:AgeBand) ON (ageBand.band)"
        ]

        with self._driver.session() as session:
            for query in index_queries:
                session.run(query)
                print(f"Index created: {query}")