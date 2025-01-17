FROM ubuntu:24.04
EXPOSE 5506

RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
COPY ./Code/App /app 
WORKDIR /app
RUN pip3 install --break-system-packages -r requirements.txt 
CMD ["python3", "main.py"]