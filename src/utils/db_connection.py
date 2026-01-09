"""Database connection utility for PostgreSQL."""
import logging
import os
import psycopg2

from dagster import EnvVar

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def get_connection_params() -> dict:
    """Get database connection parameters from environment variables."""
    return {
        "host": EnvVar("DB_HOST").get_value(),
        "port": EnvVar("DB_PORT").get_value(),
        "database": EnvVar("DB_NAME").get_value(),
        "user": EnvVar("DB_USER").get_value(),
        "password": EnvVar("DB_PASSWORD").get_value()
    }


def test_connection():
    """Test connection to PostgreSQL database and list custom schemas."""
    params = get_connection_params()

    logger.info(
        f"Attempting to connect to database: {params['database']} "
        f"at {params['host']}:{params['port']}"
    )

    query = """
    SELECT schema_name
    FROM information_schema.schemata
    WHERE schema_name NOT IN ('information_schema', 'pg_catalog')
    ORDER BY schema_name;
    """

    try:
        # Connect to database
        conn = psycopg2.connect(**params)
        cursor = conn.cursor()
        logger.info("Database connection successful!")

        # Execute query
        cursor.execute(query)
        result = cursor.fetchall()

        # Log schemas found
        schema_names = [row[0] for row in result]
        logger.info(
            f"Found {len(schema_names)} custom schemas: "
            f"{', '.join(schema_names)}"
        )

        # Close resources
        cursor.close()
        conn.close()
        logger.debug("Database connection closed")

        return True

    except psycopg2.OperationalError as e:
        logger.error(f"Connection failed: {e}")
        return False
    except Exception as e:
        logger.exception(f"Unexpected error during database connection test: {e}")
        return False


if __name__ == "__main__":
    test_connection()