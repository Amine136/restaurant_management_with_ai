# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Update and install system dependencies including OpenCV dependencies
RUN apt-get update && \
    apt-get install -y cmake g++ libgl1-mesa-glx libglib2.0-0 ffmpeg v4l-utils && \
    apt-get clean

# Set a longer timeout for pip
ENV PIP_DEFAULT_TIMEOUT=1000


# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install mysql-connector-python
RUN pip install --no-cache-dir mysql-connector-python


# Make port 80 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV NAME World

# Run main_recog.py when the container launches
CMD ["python", "main_recog.py"]
