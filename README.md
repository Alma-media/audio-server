# HTTP audio server

HTTP audio server that plays audio from a POST request.

## Prepare
- Virtual environment
```bash
python -m venv .venv
source .venv/bin/activate
uv sync
```

### Try if **ffplay** works
```bash
ffplay -nodisp -autoexit ~/my_sample_audio.wav
```

### Convert `wav` to `mp3`
```bash
ffmpeg -i ~/my_sample_audio.wav -codec:a libmp3lame -b:a 320k ~/my_sample_audio.mp3
```

## Run

### Option 1: Direct Python
```bash
uvicorn audio_server:app --host 0.0.0.0 --port 8800
```

### Option 2: Using CLI wrapper
```bash
python audio_server_cli.py --host 0.0.0.0 --port 8800
```

### Option 3: Build and install binary
```bash
# Build the binary
./build_binary.sh

# Test it
./dist/audio-server --port 8800

# Install to system (optional)
sudo cp dist/audio-server /usr/local/bin/
audio-server --port 8800
```

## Test
```bash
curl -X POST http://localhost:8800/play-audio -H "Content-Type: audio/wav" --data-binary @audio.wav
```

## Run as systemd service (Arch Linux)

### Setup

**Choose one service file:**
- `audio-server.service` - for running from source (requires virtual environment)
- `audio-server-binary.service` - for running the installed binary

1. **Copy the service file to systemd directory:**
```bash
# For source version:
sudo cp audio-server.service /etc/systemd/system/

# OR for binary version (after installing to /usr/local/bin):
sudo cp audio-server-binary.service /etc/systemd/system/audio-server.service
```

2. **Reload systemd to recognize the new service:**
```bash
sudo systemctl daemon-reload
```

3. **Enable the service to start on boot:**
```bash
sudo systemctl enable audio-server.service
```

4. **Start the service:**
```bash
sudo systemctl start audio-server.service
```

### Management
- **Check status:**
```bash
sudo systemctl status audio-server.service
```

- **View logs:**
```bash
sudo journalctl -u audio-server.service -f
```

- **Restart service:**
```bash
sudo systemctl restart audio-server.service
```

- **Stop service:**
```bash
sudo systemctl stop audio-server.service
```

- **Disable service (prevent auto-start on boot):**
```bash
sudo systemctl disable audio-server.service
```

### Notes
- The service runs on port **8800** (change in `audio-server.service` if needed)
- Audio playback requires `DISPLAY` and `PULSE_SERVER` environment variables
- The service runs as user `alma` to access your audio session
- Logs can be viewed with `journalctl`