FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

# Install npm
RUN apt-get update && \
    apt-get install -y npm && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*