from fastapi import FastAPI, Request, HTTPException
import tempfile
import subprocess
import os
import threading

app = FastAPI()

def play_audio(file_path):
    """Play audio and clean up temp file after completion"""
    def play_and_cleanup():
        try:
            print("Playing audio: " + file_path)
            # Wait for the process to complete
            result = subprocess.run([
                "ffplay", "-nodisp", "-autoexit", file_path
            ], capture_output=True, text=True)
            print(f"ffplay exit code: {result.returncode}")
            if result.stderr:
                print(f"ffplay stderr: {result.stderr}")
            if result.stdout:
                print(f"ffplay stdout: {result.stdout}")
        finally:
            print("Audio playback completed: " + file_path)
            # Clean up temp file after playback
            try:
                os.unlink(file_path)
            except Exception:
                pass
    
    # Run in background thread so HTTP response returns immediately
    thread = threading.Thread(target=play_and_cleanup, daemon=True)
    thread.start()

@app.post("/play-audio")
async def play_audio_endpoint(request: Request):
    # Read raw bytes
    audio_data = await request.body()
    
    if not audio_data:
        raise HTTPException(status_code=400, detail="No audio data")

    # Store to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        f.write(audio_data)
        f.flush()  # Ensure data is written to disk
        os.fsync(f.fileno())  # Force write to disk
        temp_file = f.name
    
    # Debug: Check file size and try to validate
    file_size = os.path.getsize(temp_file)
    print(f"Temp file created: {temp_file}, size: {file_size} bytes")
    
    # Verify it's a valid WAV by checking header
    with open(temp_file, 'rb') as f:
        header = f.read(12)
        print(f"File header (first 12 bytes): {header[:4]} ... {header[8:12]}")
        if header[:4] != b'RIFF' or header[8:12] != b'WAVE':
            print("WARNING: File doesn't have valid WAV header!")

    play_audio(temp_file)
    return {"status": "playing", "file": temp_file}
