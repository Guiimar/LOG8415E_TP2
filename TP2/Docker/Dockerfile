# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Copiez le fichier requirements.txt dans le conteneur
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Make port 80 available to the world outside this container
EXPOSE 80

# Run Benchemarking_main.py when the container launches
CMD ["python", "Benchemarking_main.py"]
