# backend/Dockerfile

# 1. Start with a standard Python 3.11 base image
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the requirements file into the container
COPY requirements.txt .

# 4. Install all the Python libraries
# --no-cache-dir makes the image smaller
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your backend application code into the container
COPY . .

# 6. Expose the port the app will run on (FastAPI default is 8000)
EXPOSE 8000

# 7. The command to run when the container starts
# This starts the Uvicorn server to run your FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
