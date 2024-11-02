# Dockerfile
FROM docker/dev-environments-default:stable-1

# Install Python 3.7 and pipenv
RUN apt-get update && \
    apt-get install -y python3.7 python3.7-dev python3-pip && \
    pip3 install pipenv

# Set the working directory
WORKDIR /app

# Copy the Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock ./

# Install dependencies
RUN pipenv install --dev --python 3.7

# Copy the rest of the application code
COPY . .

# Set the entrypoint
ENTRYPOINT ["pipenv", "run"]