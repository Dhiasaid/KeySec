# Use the official Elasticsearch image as the base image
FROM docker.elastic.co/elasticsearch/elasticsearch:7.15.2

# Set maintainer label
LABEL maintainer="your_email@example.com"

# Expose ports
EXPOSE 9200
EXPOSE 9300

# Define the command to run when the container starts
CMD ["elasticsearch"]
