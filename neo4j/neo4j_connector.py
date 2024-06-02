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
            "CREATE INDEX IF NOT EXISTS FOR (accident:Accident) ON (accident.index)",
            "CREATE INDEX IF NOT EXISTS FOR (severity:Severity) ON (severity.level)",
            "CREATE INDEX IF NOT EXISTS FOR (date:Date) ON (date.date)",
            "CREATE INDEX IF NOT EXISTS FOR (speedLimit:SpeedLimit) ON (speedLimit.limit)",
            "CREATE INDEX IF NOT EXISTS FOR (roadType:RoadType) ON (roadType.type)",
            "CREATE INDEX IF NOT EXISTS FOR (weather:Weather) ON (weather.condition)",
            "CREATE INDEX IF NOT EXISTS FOR (light:Light) ON (light.condition)",
            "CREATE INDEX IF NOT EXISTS FOR (roadSurface:RoadSurface) ON (roadSurface.condition)",
            "CREATE INDEX IF NOT EXISTS FOR (pointOfImpact:PointOfImpact) ON (pointOfImpact.impact)",
            "CREATE INDEX IF NOT EXISTS FOR (area:Area) ON (area.area)",
            "CREATE INDEX IF NOT EXISTS FOR (manoeuvre:Manoeuvre) ON (manoeuvre.type)",
            "CREATE INDEX IF NOT EXISTS FOR (vehicle:Vehicle) ON (vehicle.id)",
            "CREATE INDEX IF NOT EXISTS FOR (vehicleType:VehicleType) ON (vehicleType.type)",
            "CREATE INDEX IF NOT EXISTS FOR (make:Make) ON (make.name)",
            "CREATE INDEX IF NOT EXISTS FOR (model:Model) ON (model.name)",
            "CREATE INDEX IF NOT EXISTS FOR (driver:Driver) ON (driver.id)",
            "CREATE INDEX IF NOT EXISTS FOR (sex:Sex) ON (sex.type)",
            "CREATE INDEX IF NOT EXISTS FOR (ageBand:AgeBand) ON (ageBand.band)"
        ]

        with self._driver.session() as session:
            for query in index_queries:
                session.run(query)
                print(f"Index created: {query}")