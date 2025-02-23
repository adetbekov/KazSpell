# Stage 1: Use a devel image to extract CUPTI libraries
FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime
#FROM nvidia/cuda:11.6.2-cudnn8-devel-ubuntu20.04 AS cupti
# CUPTI libraries are located at /usr/local/cuda/extras/CUPTI/lib64 in the devel image

# Stage 2: Use the runtime image for your final build
#FROM nvidia/cuda:11.6.2-cudnn8-runtime-ubuntu20.04

# Copy CUPTI libraries from the devel image
#COPY --from=cupti /usr/local/cuda/extras/CUPTI/lib64 /usr/local/cuda/extras/CUPTI/lib64

# Add CUPTI path to LD_LIBRARY_PATH so the loader can find it
#ENV LD_LIBRARY_PATH=/usr/local/cuda/extras/CUPTI/lib64:$LD_LIBRARY_PATH

# (Continue with the rest of your Dockerfile)
# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV HOME=/metaflow
ENV PATH="/metaflow/.local/bin:/metaflow/.venv/bin:$PATH"
ENV PYTHONPATH="/metaflow/.venv/lib/python3.11/site-packages"

# Install system dependencies and add the deadsnakes PPA for Python 3.11
RUN apt-get update && apt-get install -y --no-install-recommends \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa -y \
    && apt-get update && apt-get install -y --no-install-recommends \
    python3.11 \
    python3.11-venv \
    python3.11-dev \
    python3-pip \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create necessary directories with proper permissions
RUN mkdir /logs /metaflow && chown 1000:1000 /logs /metaflow

# Set working directory and switch to non-root user (UID 1000)
WORKDIR /metaflow
USER 1000

# Copy project files with proper ownership
COPY --chown=1000:1000 . .

# Bootstrap and upgrade pip for Python 3.11, install Poetry, and install project dependencies
RUN python3.11 -m ensurepip --upgrade \
    && python3.11 -m pip install --upgrade pip \
    && python3.11 -m pip install --user poetry \
    && poetry config virtualenvs.in-project true \
    && poetry install --no-root --no-interaction --no-ansi

# Verify Poetry installation
RUN poetry --version
