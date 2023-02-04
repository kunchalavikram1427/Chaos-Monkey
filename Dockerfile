FROM python:3.9-slim
RUN pip --no-cache-dir  install requests
WORKDIR /app
COPY app.py .
CMD ["python", "app.py"]