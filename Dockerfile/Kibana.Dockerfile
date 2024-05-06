# Use the official Kibana image as the base image
FROM docker.elastic.co/kibana/kibana:7.15.2

# Set maintainer label
LABEL maintainer="your_email@example.com"

# Expose port
EXPOSE 5601

# Define the command to run when the container starts
CMD ["kibana"]
