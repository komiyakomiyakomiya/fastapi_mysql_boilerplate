#!/bin/bash

echo "Waiting for mysql to start..."
until mysql -h"$MYSQL_HOST" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" &> /dev/null
do
    sleep 1
done

cd /usr/src/app/db && \
alembic revision --autogenerate -m 'create_tables' && \
alembic upgrade head && \
python seed.py && \
pip install autopep8 # 開発用ライブラリ

cd /usr/src/app/api && uvicorn main:app --reload --port=8000 --host=0.0.0.0


# APIコンテナからDB接続
# mysql -h $MYSQL_HOST -P 3306 -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE