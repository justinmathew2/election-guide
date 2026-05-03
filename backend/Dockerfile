FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app

# Create a non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy installed packages from builder
COPY --from=builder /root/.local /home/appuser/.local
COPY . .

# Set environment variables
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PORT 8080
ENV PYTHONUNBUFFERED=1

# Change ownership to non-root user
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8080

CMD uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1 --proxy-headers

