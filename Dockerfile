FROM registry.access.redhat.com/ubi8/ubi:latest

# Install the required software
RUN yum update -y && yum install git python38 -y

# Copy Files into containers
COPY ./ .

# Install App Dependecies
RUN pip3.8 install -r requirements.txt

#Expose Ports
#Web Port
EXPOSE 8000/tcp

RUN chmod +x scraper-page.py

#Change User
USER 1001

#ENTRY
ENTRYPOINT ./scraper-page.py

