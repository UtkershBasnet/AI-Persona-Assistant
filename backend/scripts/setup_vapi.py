"""
Vapi Assistant Setup Script.

Creates a Vapi voice assistant that uses your Custom LLM URL
(FastAPI backend with RAG) instead of Vapi's built-in knowledge base.

Usage:
    python -m backend.scripts.setup_vapi --url https://your-ngrok-url.ngrok.io

Prerequisites:
    - VAPI_API_KEY set in .env
    - Backend running and publicly accessible (via ngrok for local dev)
"""
import argparse
import json
import sys
import os

import httpx

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from backend.config import get_settings


VAPI_BASE = "https://api.vapi.ai"


def create_assistant(api_key: str, server_url: str) -> dict:
    """Create a Vapi assistant with Custom LLM URL pointing to our backend."""

    payload = {
        "name": "Utkersh Basnet AI Persona",

        # First message when someone calls
        "firstMessage": (
            "Hey! Thanks for calling. I'm Utkersh's AI representative. "
            "You can ask me about his projects, experience, tech stack, "
            "or we can schedule an interview. What would you like to know?"
        ),
        "firstMessageMode": "assistant-speaks-first",

        # Model — Custom LLM pointing to our RAG backend
        "model": {
            "provider": "custom-llm",
            "url": f"{server_url}/api/vapi/chat/completions",
            "model": "llama-3.1-8b-instant",
            "metadataSendMode": "off",
            "temperature": 0.4,
            "maxTokens": 250,
            "messages": [
                {
                    "role": "system",
                    "content": "You are Utkersh Basnet's AI phone representative."
                }
            ],
        },

        # Transcriber — Deepgram Nova 2 for fast, accurate STT
        "transcriber": {
            "provider": "deepgram",
            "model": "nova-3",
            "language": "en",
        },

        # Voice — ElevenLabs (natural sounding, works with custom LLM)
        "voice": {
            "provider": "11labs",
            "voiceId": "burt",
        },

        # Call settings
        "maxDurationSeconds": 600,  # 10 min max
        "silenceTimeoutSeconds": 30,
        "endCallMessage": (
            "Thanks for calling! Don't forget, you can book a time with me "
            "at cal dot com slash utkersh basnet. Have a great day!"
        ),

        # Interruption handling
        "stopSpeakingPlan": {
            "numWords": 2,
            "voiceSeconds": 0.3,
            "backoffSeconds": 1.0,
        },
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    print("📞 Creating Vapi assistant...")
    print(f"   Custom LLM URL: {server_url}/api/vapi/chat/completions")

    response = httpx.post(
        f"{VAPI_BASE}/assistant",
        json=payload,
        headers=headers,
        timeout=30,
    )

    if response.status_code not in (200, 201):
        print(f"\n❌ Failed to create assistant: {response.status_code}")
        print(f"   {response.text}")
        sys.exit(1)

    assistant = response.json()
    print(f"\n✅ Assistant created!")
    print(f"   ID: {assistant['id']}")
    print(f"   Name: {assistant.get('name', 'N/A')}")

    return assistant


def link_twilio_number(api_key: str, assistant_id: str, settings) -> dict:
    """Link a Twilio phone number to the Vapi assistant."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN:
        print("\n⚠️  TWILIO_ACCOUNT_SID or TWILIO_AUTH_TOKEN not set in .env")
        print("   Skipping phone number setup.")
        return {}

    if not settings.TWILIO_PHONE_NUMBER:
        print("\n⚠️  TWILIO_PHONE_NUMBER not set in .env")
        print("   Skipping phone number setup.")
        return {}

    payload = {
        "provider": "twilio",
        "number": settings.TWILIO_PHONE_NUMBER,
        "twilioAccountSid": settings.TWILIO_ACCOUNT_SID,
        "twilioAuthToken": settings.TWILIO_AUTH_TOKEN,
        "assistantId": assistant_id,
        "name": "Utkersh AI Persona Line",
    }

    print(f"\n📱 Linking Twilio number {settings.TWILIO_PHONE_NUMBER}...")

    response = httpx.post(
        f"{VAPI_BASE}/phone-number",
        json=payload,
        headers=headers,
        timeout=30,
    )

    if response.status_code not in (200, 201):
        print(f"\n⚠️  Could not link phone number: {response.status_code}")
        print(f"   {response.text}")
        print(f"\n   You can manually add one from the Vapi Dashboard:")
        print(f"   https://dashboard.vapi.ai/phone-numbers")
        return {}

    phone = response.json()
    number = phone.get("number", phone.get("phoneNumber", "Unknown"))
    print(f"\n✅ Phone number linked!")
    print(f"   Number: {number}")
    print(f"   Provider: Twilio")
    print(f"   Linked to assistant: {assistant_id}")

    return phone


def main():
    parser = argparse.ArgumentParser(description="Set up Vapi voice assistant")
    parser.add_argument(
        "--url",
        required=True,
        help="Public URL of your backend (e.g., https://abc123.ngrok.io)",
    )
    parser.add_argument(
        "--skip-phone",
        action="store_true",
        help="Skip buying a phone number",
    )
    args = parser.parse_args()

    settings = get_settings()

    if not settings.VAPI_API_KEY:
        print("❌ VAPI_API_KEY not set in .env")
        sys.exit(1)

    # Clean the URL
    server_url = args.url.rstrip("/")

    print("=" * 60)
    print("  📞 Vapi Voice Assistant Setup")
    print("=" * 60)

    # Step 1: Create assistant
    assistant = create_assistant(settings.VAPI_API_KEY, server_url)

    # Save config for reference
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "voice", "vapi_config.json"
    )
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, "w") as f:
        json.dump(assistant, f, indent=2)
    print(f"   Config saved to: voice/vapi_config.json")

    # Step 2: Link Twilio phone number
    if not args.skip_phone:
        phone = link_twilio_number(settings.VAPI_API_KEY, assistant["id"], settings)

    print("\n" + "=" * 60)
    print("  🎉 Setup complete!")
    print("=" * 60)
    print(f"\n  Assistant ID: {assistant['id']}")
    print(f"  Test via web: https://dashboard.vapi.ai/assistants/{assistant['id']}")
    print(f"\n  To test locally with ngrok:")
    print(f"    1. Keep your backend running (uvicorn backend.main:app --port 8000)")
    print(f"    2. Keep ngrok running (ngrok http 8000)")
    print(f"    3. Go to the Vapi dashboard and test the assistant")
    print(f"    4. Or call the phone number if one was acquired")


if __name__ == "__main__":
    main()
