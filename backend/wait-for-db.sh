#!/bin/sh
echo "Aguardando Postgres..."
while ! nc -z db 5432; do
  sleep 1
done
echo "Postgres está pronto!"
exec "$@"
