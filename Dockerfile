# Use the official Python image as a parent image
FROM python:3.12-slim

# Install dependencies required for installing Poetry
RUN apt-get update && apt-get install -y curl

# Install Poetry using the official script
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Set the working directory in the container
WORKDIR /app

# Copy only dependency files
COPY pyproject.toml poetry.lock /app/

# Install dependencies
RUN poetry install --no-root

# Copy the rest of the application code
COPY . /app

# Expose the port the app runs on
EXPOSE 8000

# Set environment variables
ENV OPENAI_API_KEY=${OPENAI_API_KEY}
ENV OPENAI_BASE_URL=${OPENAI_BASE_URL}

# Run the application using uvicorn
CMD ["poetry", "run", "uvicorn", "src.api.v1.main:app", "--host", "0.0.0.0", "--port", "8000"]