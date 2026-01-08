#!/usr/bin/env python3
"""
Test script to verify Ollama connection and backend setup.
Run this after starting Ollama service.
"""

import httpx
import sys
import os
import asyncio

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:3b-instruct")


async def test_ollama():
    """Test connection to Ollama"""
    print("Testing Ollama connection...")
    print("=" * 50)
    
    print(f"Ollama URL: {OLLAMA_URL}")
    print(f"Model: {OLLAMA_MODEL}")
    print()
    
    try:
        # Test 1: Check if Ollama is running
        print("1. Testing Ollama service connection...")
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{OLLAMA_URL}/api/tags")
            response.raise_for_status()
            models = response.json().get("models", [])
            model_names = [m.get("name", "") for m in models]
            print(f"✅ Ollama is running!")
            print(f"Available models: {', '.join(model_names) if model_names else 'None'}")
            
            if OLLAMA_MODEL not in model_names:
                print(f"⚠️  Warning: Model '{OLLAMA_MODEL}' not found in available models")
                print(f"   Available models: {model_names}")
        
        # Test 2: Simple chat query
        print("\n2. Testing basic chat query...")
        async with httpx.AsyncClient(timeout=60.0) as client:
            payload = {
                "model": OLLAMA_MODEL,
                "messages": [
                    {"role": "user", "content": "Say 'Hello, I am working!' if you can read this."}
                ],
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 50,
                }
            }
            
            response = await client.post(f"{OLLAMA_URL}/api/chat", json=payload)
            response.raise_for_status()
            data = response.json()
            result = data.get("message", {}).get("content", "No response")
            print(f"✅ Chat query successful!")
            print(f"Response: {result}")
        
        # Test 3: System prompt test
        print("\n3. Testing with system prompt...")
        async with httpx.AsyncClient(timeout=60.0) as client:
            payload = {
                "model": OLLAMA_MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant. Be concise."
                    },
                    {"role": "user", "content": "What is 2+2?"}
                ],
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 20,
                }
            }
            
            response = await client.post(f"{OLLAMA_URL}/api/chat", json=payload)
            response.raise_for_status()
            data = response.json()
            result = data.get("message", {}).get("content", "No response")
            print(f"✅ System prompt works!")
            print(f"Response: {result}")
        
        print("\n" + "=" * 50)
        print("✅ All tests passed! Ollama is ready.")
        print("\nNext steps:")
        print("1. Start the FastAPI backend: python main.py")
        print("2. Start the Next.js frontend: npm run dev (or pnpm dev)")
        print("3. Open http://localhost:3000 and test the AI chat panel")
        
        return True
        
    except httpx.ConnectError:
        print(f"\n❌ Connection failed: Could not connect to Ollama at {OLLAMA_URL}")
        print("\nTroubleshooting:")
        print("1. Make sure Ollama is installed and running")
        print("2. Start Ollama service: ollama serve")
        print("3. Verify Ollama is running: curl http://localhost:11434/api/tags")
        print("4. Check that the model is pulled: ollama pull qwen2.5:3b-instruct")
        return False
    except Exception as e:
        print(f"\n❌ Connection failed: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure Ollama is running: ollama serve")
        print(f"2. Verify the URL is correct: {OLLAMA_URL}")
        print(f"3. Check that the model '{OLLAMA_MODEL}' is available: ollama list")
        print("4. Pull the model if needed: ollama pull qwen2.5:3b-instruct")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_ollama())
    sys.exit(0 if success else 1)
