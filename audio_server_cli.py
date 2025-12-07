#!/usr/bin/env python3
"""
CLI wrapper for audio-server to run as a standalone binary
"""
import sys
import argparse
import uvicorn

def main():
    parser = argparse.ArgumentParser(description='HTTP Audio Server')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=8800, help='Port to bind to (default: 8800)')
    parser.add_argument('--reload', action='store_true', help='Enable auto-reload (development)')
    
    args = parser.parse_args()
    
    print(f"Starting HTTP Audio Server on {args.host}:{args.port}")
    print("Press CTRL+C to quit")
    
    uvicorn.run(
        "audio_server:app",
        host=args.host,
        port=args.port,
        reload=args.reload
    )

if __name__ == "__main__":
    main()
