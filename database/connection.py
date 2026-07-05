from sqlalchemy import create_engine, text

# Update your PostgreSQL password here
DB_USER = "postgres"
DB_PASSWORD = "postgres123"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "niftyai"

DATABASE_URL = (
    f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)


def test_connection():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        print("Connected Successfully!\n")
        print(result.scalar())


if __name__ == "__main__":
    test_connection()