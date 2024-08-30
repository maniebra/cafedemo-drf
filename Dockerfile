FROM ubuntu:latest

LABEL authors="mani"

# Install necessary packages
RUN apt update && apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib

# Ensure that 'python' and 'pip' point to Python 3
RUN [ ! -e /usr/bin/python ] && ln -s /usr/bin/python3 /usr/bin/python || true
RUN [ ! -e /usr/bin/pip ] && ln -s /usr/bin/pip3 /usr/bin/pip || true

# Copy your application code to the container
COPY . /app
WORKDIR /app

# Create a virtual environment and install dependencies
RUN python -m venv venv
RUN /bin/bash -c "source venv/bin/activate && pip install -r backend/requirements.txt"

# Create the entrypoint script
RUN echo '#!/bin/bash\n\
service postgresql start\n\
sleep 5\n\
su - postgres -c "psql -c \\"CREATE USER cafeadmin WITH PASSWORD '\''root'\'';\\""\n\
su - postgres -c "psql -c \\"CREATE DATABASE cafedemo OWNER cafeadmin;\\""\n\
source venv/bin/activate\n\
export PYTHONPATH=/app\n\
python /app/backend/cafedemo/manage.py makemigrations\n\
python /app/backend/cafedemo/manage.py migrate\n\
exec "$@"' > /usr/local/bin/docker-entrypoint.sh


# Make the entrypoint script executable
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Expose necessary ports
EXPOSE 8000, 5432

# Start the PostgreSQL service and Django development server
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["bash", "-c", "source venv/bin/activate && python /app/backend/cafedemo/manage.py runserver 0.0.0.0:8000"]
