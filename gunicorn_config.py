# Gunicorn configuration for Render deployment
import multiprocessing

# Worker configuration
workers = 1  # Use only 1 worker on free tier
threads = 2  # Use 2 threads per worker
worker_class = 'gthread'  # Use threads for better memory efficiency

# Timeout configuration
timeout = 120  # Increase timeout to 120 seconds
graceful_timeout = 20

# Memory optimization
max_requests = 1000
max_requests_jitter = 50

# Logging
loglevel = 'info'
accesslog = '-'
errorlog = '-'