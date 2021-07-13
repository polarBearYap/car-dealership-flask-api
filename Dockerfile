# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# Docker file for onnxruntime-cpu
# Credit: https://hub.docker.com/_/microsoft-azureml-onnxruntimefamily
# -------------------------------------------------------------------------

FROM mcr.microsoft.com/azureml/onnxruntime:latest

# -------------------------------------------------------------------------
# End docker file for onnxruntime-cpu
# -------------------------------------------------------------------------
# -------------------------------------------------------------------------
# Deploy flask app
# -------------------------------------------------------------------------
LABEL MAINTAINER="Yap Jheng Khin polarbearyap2@gmail.com"

WORKDIR /app

ENV FLASK_APP=runserver.py
ENV FLASK_RUN_HOST=0.0.0.0

# Update the existing packages for security purposes
RUN apt-get update

# Install build-essentials packages, which are meta-packages that used for compiling softwares
RUN apt-get install -y --no-install-recommends --reinstall build-essential

# Install python3-dev to build Python extensions via `#include <Python.h>`
RUN apt-get install -y --no-install-recommends python3-dev

# To delete downloaded packages (.deb) already installed (and no longer needed)
RUN apt-get clean

# To remove all stored archives in your cache for packages that can not be downloaded anymore
RUN apt-get autoclean

COPY requirements.txt requirements.txt

# Upgrade pip installer for security purposes
RUN python3 -m pip install --upgrade pip

# Install necessary packages to run the API
RUN pip3 install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

COPY . .

# Tell Python that the environment is not restricted to ASCII data to resolve issues
# as mentioned here https://stackoverflow.com/questions/57652720/runtimeerror-click-will-abort-further-execution-because-python-3-was-configured
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# -------------------------------------------------------------------------
# End deploy flask app
# -------------------------------------------------------------------------
# Run runserver.py when the container launches
ENTRYPOINT [ "python3" ]
CMD [ "runserver.py" ]