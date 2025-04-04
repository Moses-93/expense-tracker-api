DB_FILE="database.db"

if [ ! -d "migrations" ]; then
    echo "⚠️ Alembic not initialized. Initializing..."
    alembic init migrations
fi

if [ ! -f "$DB_FILE" ]; then
    echo "⚠️ Database not found. Creating..."
    
    if [ -z "$(ls -A migrations/versions 2>/dev/null)" ]; then
        echo "📌 Creating initial migration..."
        alembic revision --autogenerate -m "Initial migration"
    fi

    echo "🔄 Applying migrations..."
    alembic upgrade head
fi

echo "🚀 Starting FastAPI..."
python -m src.main
