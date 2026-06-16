# ── Stage 1: Builder ──────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /app

# Install dependencies in isolated layer
COPY app/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ── Stage 2: Final image ──────────────────────────────────────────
FROM python:3.11-slim AS final

# Security: run as non-root user
RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /root/.local /home/appuser/.local

# Copy application code
COPY app/app.py .

# Set ownership
RUN chown -R appuser:appuser /app

USER appuser

# Environment variables
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PORT=8080
ENV ENVIRONMENT=production

EXPOSE 8080

# Health check — Docker will monitor this
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')"

# Production server — not Flask dev server
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "60", "app:app"]