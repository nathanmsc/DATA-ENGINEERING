https://github.com/Stirling-Tools/Stirling-PDF

docker run -d \
  -p 8080:8080 \
  -v  /mnt/d/Documents/stirling/trainingData:/usr/share/tessdata \
  -v  /mnt/d/Documents/stirling/extraConfigs:/configs \
  -v  /mnt/d/Documents/stirling/logs:/logs \
  -e DOCKER_ENABLE_SECURITY=false \
  -e INSTALL_BOOK_AND_ADVANCED_HTML_OPS=false \
  -e LANGS=en_GB \
  --name stirling-pdf \
  frooodle/s-pdf:latest
