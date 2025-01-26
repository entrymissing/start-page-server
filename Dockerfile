# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set environment variables
ENV SECRET_KEY='003e5b83e479f107fe33b11afc756d761b56764183843c3b632c71af1cc7cf83'
ENV DEBUG='False'

# Expose the port the app runs on
EXPOSE 8091

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8091", "--insecure"]
