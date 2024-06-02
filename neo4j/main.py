import time
from neo4j_connector import Neo4jConnection
from data_loader import load_data
from node_creator import create_nodes
from timer import format_time
import queries

# Constants
URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "password"
CSV_PATH = "../data/merged_information_clean.csv"

def main():
    conn = Neo4jConnection(URI, USERNAME, PASSWORD)

    try:
        # Create indexes
        conn.create_indexes()

        # Load data and insert into the database
        df = load_data(CSV_PATH)
        #df = load_data(CSV_PATH, 25000)

        start_time = time.time()
        create_nodes(df, conn, 1000)
        end_time = time.time()

        duration = end_time - start_time
        formatted_duration = format_time(duration)
        print(f"Total data insertion completed in {formatted_duration}")
    finally:
        conn.close()


def get_all_node_types():
    conn = Neo4jConnection(URI, USERNAME, PASSWORD)
    
    try:
        query_nodes = """
        CALL db.labels() YIELD label
        RETURN label
        """

        query_relationships = """
        CALL db.relationshipTypes() YIELD relationshipType
        RETURN relationshipType
        """

        node_labels = conn.execute_read_query(query_nodes)
        relationships = conn.execute_read_query(query_relationships)

        
        print("\nNode Labels:")
        for label in node_labels:
            print(f"- {label}")

        print("\nRelationships:")
        for relationship in relationships:
            print(f"- {relationship}")

    finally:
        conn.close()

def run_query(query):
    conn = Neo4jConnection(URI, USERNAME, PASSWORD)
    try:
        result = conn.execute_read_query(query[0], query[1])
        print("Query results:")
        index = 1
        for record in result:
            print(f"# {index}:")
            index += 1
            print(record)
    finally:
        conn.close()


def menu():
    while True:
        print("\nMenu:")
        print("=====================================")
        print("1. Populate database with data")
        print("2. Get all node types")
        print("3. Run a query")
        print("4. Exit\n")
        choice = input("Enter your choice: \n")
        
        if choice == '1':
            main()
        elif choice == '2':
            get_all_node_types()
        elif choice == '3':
            while True:
                print("\nQueries:")
                print("=====================================")
                print("1. Get all car accidents by make and accident year")
                print("2. Get longitude and latitude for all car accidents by year")
                print("3. Get accident by index")
                print("4. Go back to main menu\n")
                choice = input("Enter your choice: \n")
                if choice == '1':
                    make = input("Enter car make: ").upper()
                    year = input("Enter accident year: ")
                    run_query(queries.get_all_car_accidents_by_make_and_accident_year(make, year))
                elif choice == '2':
                    year = input("Enter accident year: ")
                    run_query(queries.get_longitude_and_latitude_for_all_car_accidents_by_year(year))
                elif choice == '3':
                    index = input("Enter accident index: ")
                    run_query(queries.get_accident_by_index(index))
                elif choice == '4':
                    break
                else:
                    print("Invalid choice. Please try again.")
        elif choice == '4':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()