FROM registry.access.redhat.com/ubi8/ubi:latest

#ENV Variables
ENV APP_MODULE runapp:app
ENV APP_CONFIG gunicorn/gunicorn.conf.py
ENV APP_SCRIPT ./runapp.sh
ENV DOCKERFILE_RUN true

# Install the required software
RUN yum update -y && yum install git python38 -y

#Make Application Directory
RUN mkdir ./app && cd ./app

# Copy Files into containers
COPY ./ ./app

#WORKDIR
WORKDIR ./app

# Install App Dependecies
RUN pip3.8 install -r requirements.txt

#Expose Ports
#Web Port
EXPOSE 5000/tcp

#Change Permissions to allow not root-user work
RUN chmod -R g+rw ./ && chmod +x runapp.sh

#Change User
USER 1001

#ENTRY
ENTRYPOINT $APP_SCRIPT
