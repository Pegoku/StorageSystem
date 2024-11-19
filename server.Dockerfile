FROM python:3.12.7-bookworm

# Set the working directory
WORKDIR /app

COPY ./Code/Server /app

COPY ./requirements.txt /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose the port
EXPOSE 5000

# Run the application
CMD ["python", "main.py"]

