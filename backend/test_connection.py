#!/usr/bin/env python3
"""
Test script to verify LM Studio connection and backend setup.
Run this after starting LM Studio server.
"""

from openai import OpenAI
import sys
import os
import httpx

def test_lm_studio():
    """Test connection to LM Studio"""
    print("Testing LM Studio connection...")
    print("=" * 50)
    
    # Use environment variables or defaults
    lm_studio_url = os.getenv("LM_STUDIO_URL", "http://10.187.15.14:1234/v1")
    model_name = os.getenv("LM_STUDIO_MODEL", "qwen2.5-7b-instruct-1m")
    
    print(f"LM Studio URL: {lm_studio_url}")
    print(f"Model: {model_name}")
    print()
    
    try:
        # Create httpx client without proxies to avoid initialization errors
        # Note: httpx.Client doesn't take base_url, OpenAI client handles that
        http_client = httpx.Client(
            proxies=None,  # Explicitly disable proxies
            timeout=60.0
        )
        
        client = OpenAI(
            base_url=lm_studio_url,
            api_key="not-needed",
            http_client=http_client
        )
        
        # Test simple query
        print("1. Testing basic connection...")
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "user", "content": "Say 'Hello, I am working!' if you can read this."}
            ],
            max_tokens=50,
        )
        
        result = response.choices[0].message.content
        print(f"✅ Connection successful!")
        print(f"Response: {result}")
        
        # Test with system prompt
        print("\n2. Testing with system prompt...")
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Be concise."
                },
                {"role": "user", "content": "What is 2+2?"}
            ],
            max_tokens=20,
        )
        
        result = response.choices[0].message.content
        print(f"✅ System prompt works!")
        print(f"Response: {result}")
        
        print("\n" + "=" * 50)
        print("✅ All tests passed! LM Studio is ready.")
        print("\nNext steps:")
        print("1. Start the FastAPI backend: python main.py")
        print("2. Start the Next.js frontend: npm run dev")
        print("3. Open http://localhost:3000 and test the AI chat panel")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Connection failed: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure LM Studio is running")
        print("2. Check that the server is started (Developer tab → Start Server)")
        print(f"3. Verify the server is on {lm_studio_url.replace('/v1', '')}")
        print(f"4. Check that you have the model '{model_name}' loaded")
        print("5. Set environment variables if using different URL/model:")
        print("   export LM_STUDIO_URL=http://your-ip:1234/v1")
        print("   export LM_STUDIO_MODEL=your-model-name")
        return False

if __name__ == "__main__":
    success = test_lm_studio()
    sys.exit(0 if success else 1)
