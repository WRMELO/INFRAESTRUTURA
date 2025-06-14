version: '3.8'

  

services:

jupyter-cpu:

image: jupyter-cpu:latest

container_name: jupyter_cpu

ports:

- "8888:8888"

environment:

JUPYTER_ENABLE_LAB: "yes"

JUPYTER_TOKEN: "senhasegura"

volumes:

- /home/wrm/INFRAESTRUTURA:/home/jovyan/work:rshared # MODIFICAÇÃO APLICADA AQUI

restart: unless-stopped

  

minio:

image: minio/minio:latest

container_name: minio

environment:

MINIO_ROOT_USER: admin

MINIO_ROOT_PASSWORD: senhasegura

ports:

- "9000:9000"

- "9001:9001"

volumes:

- minio_data:/data

command: server /data --console-address ":9001"

restart: unless-stopped

  

database-services:

image: postgres:15-alpine

container_name: postgres_db

environment:

POSTGRES_USER: postgres

POSTGRES_PASSWORD: senhasegura

POSTGRES_DB: postgres

ports:

- "5432:5432"

volumes:

- db_data:/var/lib/postgresql/data

restart: unless-stopped

  

mongo:

image: mongo:7.0

container_name: mongo_db

environment:

MONGO_INITDB_ROOT_USERNAME: root

MONGO_INITDB_ROOT_PASSWORD: senhasegura

ports:

- "27017:27017"

volumes:

- mongo_data:/data/db

restart: unless-stopped

  

vector-database:

image: vector-database:latest

container_name: vector_database

ports:

- "8200:8200"

restart: unless-stopped

  

gdrive-sync:

image: rclone/rclone:latest

container_name: gdrive_sync_mount

privileged: true

environment:

- PUID=1000

- PGID=1000

volumes:

- ./rclone_config:/config/rclone

- ./gdrive_local_mount:/mnt/gdrive:shared

command:

- mount

- "gdrive_remote:"

- /mnt/gdrive

- --allow-other

- --allow-non-empty

- --dir-cache-time

- 72h

- --poll-interval

- 15s

- --vfs-cache-mode

- full

- --vfs-cache-max-age

- 7d

- --vfs-cache-max-size

- 50G

- --vfs-read-chunk-size

- 64M

- --vfs-read-chunk-size-limit

- "off"

- --umask

- "002"

- --log-level

- INFO

restart: unless-stopped

  

volumes:

db_data:

minio_data:

mongo_data: