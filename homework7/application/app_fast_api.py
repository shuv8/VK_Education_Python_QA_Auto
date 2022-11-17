#!/usr/bin/env python3
import os

import requests
import uvicorn
from fastapi import FastAPI, Response, status
from pydantic import BaseModel


class User(BaseModel):
    name: str
    surname: str
    age: int | None


class UserUPD(BaseModel):
    age: int


app = FastAPI()

app_data = {}
app_user_data = {}
user_id_seq = 1


@app.get('/')
async def root():
    return {"Status": "Working!"}


@app.get('/get_user')
async def get_user(response: Response, name: str = None, surname: str = None):
    global app_user_data
    if name is None or surname is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return 'No name or surname provided. Use query parameters'
    if user_id := app_data.get(surname + ' ' + name):
        if age := app_user_data[user_id]['age']:
            return {'user_id': user_id, 'name': app_user_data[user_id]['name'],
                    'surname': app_user_data[user_id]['surname'], 'age': age}
        else:
            age_host = os.environ.get('STUB_HOST')
            age_port = os.environ.get('STUB_PORT')
            try:
                age = requests.get(
                    f'http://{age_host}:{age_port}/get_age/{name}').json()
            except Exception as e:
                print(f'Unable to get age from external system:\n{e}')
            app_user_data[user_id]['age'] = age
            response.status_code = status.HTTP_200_OK
            return {'user_id': user_id, 'name': app_user_data[user_id]['name'],
                    'surname': app_user_data[user_id]['surname'], 'age': age}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f'User {surname} {name} not found'


@app.post('/add_user')
async def add_user(user: User, response: Response):
    global user_id_seq
    global app_user_data
    user_full_name = user.surname + ' ' + user.name
    if user_full_name not in app_data:
        app_data[user_full_name] = user_id_seq
        app_user_data[user_id_seq] = {'name': user.name,
                                      'surname': user.surname,
                                      'age': user.age}
        user_id_seq += 1
        response.status_code = status.HTTP_201_CREATED
        return {'user_id': app_data[user_full_name]}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return f'User {user_full_name} already exists - id: {app_data[user_full_name]}'


@app.put('/update_user')
async def update_user(response: Response, new_user: UserUPD, name: str = None, surname: str = None):
    global user_id_seq
    global app_user_data
    if name is None or surname is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return 'No name or surname provided. Use query parameters'
    user_full_name = surname + ' ' + name
    if user_full_name not in app_data:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f'User {surname} {name} not found'
    user_id = app_data[user_full_name]
    old_age = app_user_data[user_id]['age']
    app_user_data[user_id]['age'] = new_user.age
    response.status_code = status.HTTP_202_ACCEPTED
    return f'Users {surname} {name} was {old_age}, now it is {new_user.age}'


@app.delete('/delete_user')
async def delete_user(user: User, response: Response):
    global app_user_data
    global app_data
    user_full_name = user.surname + ' ' + user.name
    if user_full_name not in app_data:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f'User {user_full_name} not found'
    app_user_data.pop(app_data[user_full_name])
    app_data.pop(user_full_name)
    response.status_code = status.HTTP_204_NO_CONTENT


if __name__ == '__main__':
    host = os.environ.get('APP_HOST', '127.0.0.1')
    port = os.environ.get('APP_PORT', default=5000)
    uvicorn.run(app, host=host, port=int(port))
