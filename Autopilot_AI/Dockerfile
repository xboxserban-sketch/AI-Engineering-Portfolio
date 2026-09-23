# Use a lightweight NGINX image to serve the frontend
FROM nginx:alpine

# Copy the frontend files to the default NGINX public directory
COPY index.html /usr/share/nginx/html/
COPY app.js /usr/share/nginx/html/
COPY style.css /usr/share/nginx/html/

# Expose port 80
EXPOSE 80

# Start NGINX
CMD ["nginx", "-g", "daemon off;"]
