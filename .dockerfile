# Dockerfile
FROM docker/dev-environments-default:stable-1

# Install pipenv
RUN pip install pipenv

# Set the working directory
WORKDIR /app

# Copy the Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock ./

# Install dependencies
RUN pipenv install --dev

# Copy the rest of the application code
COPY . .

# Set the entrypoint
ENTRYPOINT ["pipenv", "run"]