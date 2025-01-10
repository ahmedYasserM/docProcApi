# Stage 1: Build
FROM python:3.13-alpine as build

# Install uv
RUN apk add uv

# Set the working directory
WORKDIR /app

# Copy the pyproject.toml file
COPY pyproject.toml .

# Install dependencies using UV
RUN uv sync

# Copy the rest of the application code
COPY . .

# Change to the core directory
WORKDIR /app/core

# Run migrations
RUN uv run manage.py makemigrations
RUN uv run manage.py migrate

# Stage 2: Runtime
FROM python:3.13-alpine

# Set the working directory
WORKDIR /app

# Copy only the installed dependencies from the build stage
COPY --from=build /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=build /usr/local/bin /usr/local/bin

# Copy the application code
COPY --from=build /app /app

# Change to the core directory
WORKDIR /app/core

# Run the server
CMD ["uv", "run", "manage.py", "runserver", "0.0.0.0:8000"]
