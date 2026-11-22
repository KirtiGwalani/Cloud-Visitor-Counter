from flask import Flask, jsonify
import redis
import os

app = Flask(__name__)

def get_redis():
    return redis.Redis(
        host=os.getenv("REDIS_HOST", "redis"),
        port=6379,
        decode_responses=True
    )

@app.route("/")
def home():
    count = get_redis().incr("visitor_count")
    return f"""
    <html>
    <head><title>Cloud Visitor Counter</title></head>
    <body style="text-align:center;font-family:Arial;background:#eaf2ff;padding:80px">
    <h1>Cloud Visitor Counter</h1>
    <h2 style="font-size:60px;color:green">{count}</h2>
    <h3>Total Visitors</h3>
    <p>Powered by Flask, Redis, Docker and Kubernetes</p>
    </body>
    </html>
    """

@app.route("/health")
def health():
    return jsonify(status="healthy")

@app.route("/api/count")
def count():
    return jsonify(visitors=get_redis().get("visitor_count") or 0)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
