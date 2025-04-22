from fastapi import FastAPI
import redis
import os

app = FastAPI()

# Connect to Redis using environment variables (defaults to Redis service name)
redis_host = os.getenv("REDIS_HOST", "redis")
redis_port = int(os.getenv("REDIS_PORT", 6379))
r = redis.Redis(host=redis_host, port=redis_port)

@app.get("/")
def read_root():
    # Read from Redis
    value = r.get("mykey")
    if value:
        return {"message": f"Value from Redis: {value.decode()}"}
    else:
        return {"message": "No value set in Redis"}

@app.get("/set")
def set_value():
    # Write to Redis
    r.set("mykey", "Hello from FastAPI via Redis!")
    return {"message": "Value set in Redis"}
