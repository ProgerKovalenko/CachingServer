import argparse

def main():

    parser = argparse.ArgumentParser(description='Caching Proxy Server')

    parser.add_argument("--port", type=int, default=3000, help = "Local port for start server")
    parser.add_argument("--origin", type=str, required= True, help = "URL server, that we proxy")
    parser.add_argument("--clear-cache", action='store_true', help = "Clear cache")

    args = parser.parse_args()

    print(f"Start server on port {args.port}")
    print(f"Proxy server on {args.origin}")

    if args.clear_cache:
        print("Clearing cache")


if __name__ == "__main__":
    main()
