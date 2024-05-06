# Use a base image appropriate for your agent's runtime environment
FROM python:3.9-slim

# Set environment variables
ENV APP_HOME /app
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR $APP_HOME

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the agent's source code into the container
COPY . .

# Expose any necessary ports
# EXPOSE 8080

# Define the command to run the agent
CMD ["python", "agent.py"]
