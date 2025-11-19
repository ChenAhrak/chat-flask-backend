# base image
FROM python:3.11-slim

# working directory
WORKDIR /app

# create non-root user 
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# copy req
COPY requirements.txt .

# dependencies
RUN pip install --no-cache-dir -r requirements.txt

# application files
COPY --chown=appuser:appuser Client/ ./Client/
COPY --chown=appuser:appuser app.py .

# switch to non-root user
USER appuser

#entrypoint
ENTRYPOINT [ "python", "app.py" ]