# Docker makes isolated environment called container, and allowed applications to run in any 
# different devices, which has different settings, in same virtual environment.
# And this file is actually setting that environment.

# Docker image that has python runtime environment pre-installed, to execute python software.
FROM python:3.13.0a5-slim

# Path inside Unix system.
WORKDIR /usr/src/djangobnb_backend

# Setting environment variables. Prevent python from creating '.pyc' files
ENV PYTHONDONTWRITEBYTECODE 1

# Setting python unbuffered, which means printing(or logging) immedeiately  to terminal or files.
# It is important when we need to monitor behavior of application in real-time.
ENV PYTHONUNBUFFERED 1

# Run is executed when <docker build> command is typed in terminal to create docker 
# image(which is used to create container), and commit changes to new image layer.
RUN pip install --upgrade pip

# Copy the 'requirements.txt' file to the current working directory, inside the docker image
# being built.
COPY ./requirements.txt .

# Copy entire django project into this folder location.
COPY . .