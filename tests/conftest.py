import pytest
import requests
import helper
import urls


@pytest.fixture(scope='function')
def create_and_delete_new_user():
    user = helper.generate_user_data()
    reg_response = requests.post(urls.BASE_URL + urls.CREATE_USER, data=user)
    token = reg_response.json()['accessToken']
    yield token, user
    requests.delete(urls.BASE_URL + urls.DELETE_USER, headers={'Authorization': token})
