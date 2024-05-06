# Use the official Nginx image as the base image
FROM nginx:latest

# Set maintainer label
LABEL maintainer="your_email@example.com"

# Copy custom Nginx configuration file
COPY nginx.conf /etc/nginx/nginx.conf

# Expose ports
EXPOSE 80
EXPOSE 443

# Define the command to run when the container starts
CMD ["nginx", "-g", "daemon off;"]
