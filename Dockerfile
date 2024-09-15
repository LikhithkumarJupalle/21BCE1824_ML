FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all the contents from the current directory to the container's working directory
COPY . /app

# Install dependencies listed in the requirements file without cache to reduce image size
RUN pip install --no-cache -r requirements.txt

# Expose the container's port 8000 to the host machine
EXPOSE 8000

# Set the default command to run the FastAPI app with Uvicorn, specifying the host and port
ENTRYPOINT ["uvicorn", "app:app", "--host=0.0.0.0", "--port=8000"]
