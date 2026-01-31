import argparse
import httpx
from fastapi import FastAPI,Request,Response
import uvicorn
from urllib.parse import urlparse

app = FastAPI()
ORIGIN_URL = ""

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_logic(request: Request, path: str):
    target_url = f"{ORIGIN_URL.rstrip('/')}/{path.lstrip('/')}"


    domain = urlparse(ORIGIN_URL).netloc


    headers = {
        "Host": domain,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "*/*"
    }

    print(f"\nDebug: Path {path} -> Target {target_url}")
    print(f"Debug: Setting Host to {domain}")


    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=await request.body(),
                timeout=15.0
            )

        print(f"Origin Status: {response.status_code}")

        return Response(
            content=response.content,
            status_code=response.status_code,
            headers={
                "X-Cache": "MISS",
                "Content-Type": response.headers.get("Content-Type", "application/json")
            }
        )
    except Exception as e:
        print(f"Error during proxy: {e}")
        return Response(content=f"Proxy Error: {e}", status_code=500)


def main():
    global ORIGIN_URL
    parser = argparse.ArgumentParser(description='Caching Proxy Server')
    parser.add_argument("--port", type=int, default=3000, help = "Local port for start server")
    parser.add_argument("--origin", type=str, required= True, help = "URL server, that we proxy")
    parser.add_argument("--clear-cache", action='store_true', help = "Clear cache")
    args = parser.parse_args()


    ORIGIN_URL = args.origin.strip("/")


    print(f"Starting proxy on port {args.port}, origin: {ORIGIN_URL}")
    uvicorn.run(app, host= "127.0.0.1", port=args.port)


    if args.clear_cache:
        print("Clearing cache")


if __name__ == "__main__":
    main()
