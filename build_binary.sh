#!/bin/bash
# Build script for creating audio-server binary

set -e

echo "Installing PyInstaller..."
pip install pyinstaller

echo "Building binary..."
pyinstaller --onefile \
    --name audio-server \
    --add-data "audio_server.py:." \
    --hidden-import fastapi \
    --hidden-import uvicorn \
    --hidden-import uvicorn.logging \
    --hidden-import uvicorn.loops \
    --hidden-import uvicorn.loops.auto \
    --hidden-import uvicorn.protocols \
    --hidden-import uvicorn.protocols.http \
    --hidden-import uvicorn.protocols.http.auto \
    --hidden-import uvicorn.protocols.websockets \
    --hidden-import uvicorn.protocols.websockets.auto \
    --hidden-import uvicorn.lifespan \
    --hidden-import uvicorn.lifespan.on \
    audio_server_cli.py

echo ""
echo "Binary created at: dist/audio-server"
echo "Test it with: ./dist/audio-server"
echo "Install it with: sudo cp dist/audio-server /usr/local/bin/"
