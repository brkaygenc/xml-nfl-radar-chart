from src.database.queries import list_tables, get_table_schema

def main():
    print("\nListing all tables in the database:")
    tables = list_tables()
    for table in tables:
        print(f"\n=== Table: {table} ===")
        schema = get_table_schema(table)
        for column in schema:
            nullable = "NULL" if column['nullable'] == 'YES' else "NOT NULL"
            print(f"{column['column']}: {column['type']} {nullable}")

if __name__ == '__main__':
    main() 