import os

QUEUE_NAME = os.getenv("QUEUE_NAME", "-SpotTheDifference:inference")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
INFERENCE_API_URL = os.getenv("INFERENCE_API_URL", "http://localhost:8009/api/v1/analyze")


def process_job(message: bytes | str) -> dict:
    # TODO: Validate a queued job, call inference, and persist its result.
    return {"status": "placeholder", "message": message.decode() if isinstance(message, bytes) else message}


def main() -> None:
    # TODO: Connect to Redis and consume QUEUE_NAME.
    print(f"Worker placeholder for queue {QUEUE_NAME} at {REDIS_URL}; API {INFERENCE_API_URL}")


if __name__ == "__main__":
    main()
