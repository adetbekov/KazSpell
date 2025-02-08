FROM python:3.9-slim

# Set AWS credentials as environment variables (for testing only)
ENV AWS_ACCESS_KEY_ID=fY4vB53y2PW9brRMd9ig
ENV AWS_SECRET_ACCESS_KEY=ULPhltAXq3SAqLl4pUIImz9kUa8ZIP01wu5dgchs
ENV METAFLOW_S3_ENDPOINT_URL=http://10.243.219.93:32000

# Install Metaflow (and any other dependencies)
RUN pip install poetry
RUN poetry install

# (Optionally, copy an entrypoint script if needed)
# COPY entrypoint.sh /entrypoint.sh
# RUN chmod +x /entrypoint.sh
# ENTRYPOINT ["/entrypoint.sh"]

CMD ["python"]