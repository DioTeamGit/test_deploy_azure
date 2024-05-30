FROM python:3.9-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN apk add --no-cache \
    build-base \
    libffi-dev \
    gcc \
    gfortran \
    musl-dev \
    linux-headers \
    g++ \
    openblas-dev \
    python3-dev \
    freetype-dev \
    lapack-dev \
    make

# Install pip
RUN python -m ensurepip
RUN pip install --no-cache --upgrade pip

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV FLASK_APP=app.py

# Run app.py when the container launches
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "80"]