# syntax=docker/dockerfile:1
# base python image
FROM python:3.10.12-slim-buster
# enviroment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Update the package list and install geo dependencies
RUN apt-get update && apt-get install -y \
    binutils \
    libproj-dev \
    gdal-bin \
    libgdal-dev \
    python3-gdal \
    libgeos-dev \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# RUN wget https://download.osgeo.org/geos/geos-3.8.4.tar.bz2 \
#     tar xjf geos-3.8.4.tar.bz2 \
#     cd geos-3.8.4 \
#     mkdir build \
#     cd build \
#     cmake -DCMAKE_BUILD_TYPE=Release .. \
#     cmake --build . \
#     sudo cmake --build . --target install \

# working directory
WORKDIR /app

# copy requirements.txt and install requirements
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

RUN chmod +x /app/entrypoint.sh

# entrypoint
CMD ["bash", "-c", "/app/entrypoint.sh"]
# pre-requisite to psycopg2
#sudo apt-get install libpq-dev
# update pip










