FROM jenkins/jenkins:lts-jdk17

USER root

# Install Python 3 and pip
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Verify Python installation
RUN python3 --version && pip3 --version

USER jenkins
