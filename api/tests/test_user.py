import json
import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
# ↑↓ 等価 (TestClient)
# from starlette.testclient import TestClient
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from main import app
from utils import utils
from database import SessionLocal


@pytest.fixture
def client():
    client = TestClient(app)
    return client


@pytest.fixture
def db():
    db = SessionLocal()
    return db


def test_read_user_exists(client):
    user_id = 1
    res = client.get(f'/users/{user_id}/')
    res_json = res.json()

    # assert response.status_code == 200
    assert res.status_code == HTTP_200_OK
    assert res_json['id'] == user_id
    assert res_json['username'] == 'Sousou'
    assert res_json['books'][0]['title'] == 'book1'
    assert res_json['books'][1]['title'] == 'book2'
    assert res_json['del_flg'] == 0


def test_read_user_not_exists(client):
    user_id = 4
    res = client.get(f'/users/{user_id}/')
    assert res.status_code == HTTP_404_NOT_FOUND


def test_read_user_deleted(client):
    user_id = 2
    res = client.get(f'/users/{user_id}/')
    assert res.status_code == HTTP_404_NOT_FOUND


def test_read_users(client):
    res = client.get('/users/')
    res_json = res.json()
    assert res.status_code == HTTP_200_OK
    assert res_json[0]['id'] == 1
    assert res_json[0]['username'] == 'Sousou'
    assert res_json[0]['books'][0]['title'] == 'book1'
    assert res_json[0]['books'][1]['title'] == 'book2'
    assert res_json[0]['del_flg'] == 0
    assert res_json[1]['id'] == 3
    assert res_json[1]['username'] == 'Sonken'
    assert res_json[1]['books'] == []
    assert res_json[1]['del_flg'] == 0


def test_create_user(client, db):
    username = 'Ryohu'
    user_obj = {'username': username}
    res = client.post('/users/', json=user_obj)
    res_json = res.json()
    assert res.status_code == HTTP_200_OK
    assert res_json['username'] == username
    assert res_json['books'] == []
    assert res_json['del_flg'] == 0
    # もとに戻す
    utils.delete_users_by_usernames(usernames=[username], db=db)


def test_update_user_exists(client):
    user_id = 1
    username_original = 'Sousou'
    username_new = 'Ryohu'
    user_obj = {'username': username_new}
    res = client.put(f'/users/{user_id}/', json=user_obj)
    res_json = res.json()
    assert res.status_code == HTTP_200_OK
    assert res_json['id'] == user_id
    assert res_json['username'] == username_new
    # もとに戻す
    user_obj['username'] = username_original
    res = client.put(f'/users/{user_id}/', json=user_obj)


def test_update_user_not_exists(client):
    user_id = 4
    username_new = 'Ryohu'
    user_obj = {'username': username_new}
    res = client.put(f'/users/{user_id}/', json=user_obj)
    assert res.status_code == HTTP_404_NOT_FOUND


def test_update_user_deleted(client):
    user_id = 2
    username_new = 'Ryohu'
    user_obj = {'username': username_new}
    res = client.put(f'/users/{user_id}/', json=user_obj)
    assert res.status_code == HTTP_404_NOT_FOUND


def test_delete_user_exists(client, db):
    user_id = 1
    res = client.delete(f'/users/{user_id}/')
    res_json = res.json()
    assert res.status_code == HTTP_200_OK
    assert res_json['id'] == user_id
    assert res_json['username'] == 'Sousou'
    assert res_json['books'] == []
    assert res_json['del_flg'] == 1

    utils.update_users_delflg_by_ids(ids=[user_id], del_flg=0, db=db)
    utils.update_books_user_id_by_ids(ids=[1, 2], user_id=1, db=db)


def test_delete_user_not_exists(client):
    user_id = 4
    res = client.delete(f'/users/{user_id}/')
    assert res.status_code == HTTP_404_NOT_FOUND


def test_delete_user_deleted(client):
    user_id = 2
    res = client.delete(f'/users/{user_id}/')
    assert res.status_code == HTTP_404_NOT_FOUND
