docker run -p 8000:8000 \
  -v $(pwd)/workspace:/app/workspace \
  --name servequery-service \
  --detach \
  ServeQuery-service:latest