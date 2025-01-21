#!/bin/bash

# Variables
# Store all backups in the Backups directory
BACKUP_DIR="/srv/Dancina/Dancina/Backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/dancina_db_backup_$TIMESTAMP.sql"
ZIP_FILE="$BACKUP_FILE.gz"
DOCKER_BIN="/usr/bin/docker"
DOCKER_CONTAINER="django_dancina_db"  # Name of the PostgreSQL container
POSTGRES_USER="postgres"             # PostgreSQL username
POSTGRES_DB="dancina_db"             # PostgreSQL database name

# Create a backup and compress it
docker exec $DOCKER_CONTAINER pg_dump -U $POSTGRES_USER $POSTGRES_DB > $BACKUP_FILE
gzip $BACKUP_FILE

# Optional: Remove backups older than 7 days
find $BACKUP_DIR -type f -name "dancina_db_backup_*.sql.gz" -mtime +7 -exec rm -f {} \;

echo "Backup created and compressed at $ZIP_FILE"
