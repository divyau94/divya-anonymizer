FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

ENTRYPOINT ["/bin/sh", "-c", "\
  if [ \"$1\" = 'generate' ]; then \
    shift; \
    exec python src/generator.py \"$@\"; \
  elif [ \"$1\" = 'anonymize' ]; then \
    shift; \
    exec python src/anonymizer.py \"$@\"; \
  else \
    echo \"Usage: $0 <generate|anonymize> [options]\" >&2; \
    exit 1; \
  fi", "--"]

