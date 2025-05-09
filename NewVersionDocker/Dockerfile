# base image
FROM python:3.11-slim	

# working directory
WORKDIR /app

# copying requirements
COPY requirements.txt .

# installing dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copying source code
COPY . .

# running Django Development server (for local)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
