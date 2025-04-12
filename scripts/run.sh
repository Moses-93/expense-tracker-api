# Wait 5 seconds before launching the FastAPI to give the database time to start
sleep 5

echo "🔄 Applying migrations..."
alembic upgrade head

echo "🚀 Starting FastAPI..."
python -m src.main
