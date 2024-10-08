set -e

echo "Run Application"

uvicorn fastapi_chat.main:app \
    --host=0.0.0.0 \
    --port=80 \
    --workers=2 \
    --reload \
    --log-level=debug \
    --use-colors \
    --reload-delay=5.0
