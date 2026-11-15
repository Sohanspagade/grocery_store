import os
import httpx
import asyncio
import json

async def main():
    api_key = os.getenv("OPENROUTER_API_KEY", "")
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            'https://openrouter.ai/api/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'openrouter/auto',
                'messages': [{'role': 'user', 'content': 'hello'}]
            }
        )
        print("Status:", response.status_code)
        print("Response:", json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    asyncio.run(main())
