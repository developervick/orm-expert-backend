#!/bin/bash

# Generate OpenAPI schema
echo "📝 Generating OpenAPI schema..."
python manage.py spectacular --file /app/schema.yml --color

# Check if generation was successful
if [ $? -eq 0 ]; then
    echo "✅ Schema generated successfully at /app/schema.yml"
else
    echo "❌ Schema generation failed!"
    exit 1
fi

# Start Django server
echo "🚀 Starting Django server..."
python manage.py runserver 0.0.0.0:8000