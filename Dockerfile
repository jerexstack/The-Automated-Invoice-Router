# 1. Use an official, lightweight Python runtime blueprint
FROM python:3.11-slim

# 2. Set the internal working directory inside the isolated container
WORKDIR /app

# 3. Copy just the dependency manifest first (Optimizes Docker build caching)
COPY requirements.txt .

# 4. Install production dependencies cleanly without saving cache junk
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your local application code into the container image
COPY . .

# 6. Open up the container's internal firewall port to match our gateway
EXPOSE 8000

# 7. The execution engine command that fires up Uvicorn when the container boots
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]