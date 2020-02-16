import pytest
import requests


@pytest.fixture
def populate_db(base_url):

    user_to_enter = {
            "name": "Ervin Howell",
            "username": "Antonette",
            "email": "Shanna@melissa.tv"
            }

    inserted_ids = []

    def _insert_item(num_entries_to_insert=1):

        users = dict()
        users['data'] = [user_to_enter for _ in range(num_entries_to_insert)]

        result = requests.post(base_url, json=users)

        assert result.status_code == 200
        last_created_id = int(result.headers['location'].split('/')[-1])

        inserted_ids.extend(list(
            range(last_created_id - num_entries_to_insert, last_created_id + 1)))

    yield _insert_item

    for id_ in inserted_ids:
        base_url.simulate_delete('/{}'.format(id_))


def test_users_get_list(base_url, populate_db):

    NUM_RECORDS = 3
    populate_db(num_entries_to_insert=NUM_RECORDS)

    result = requests.get(base_url)

    assert requests.status_code == 200
    assert len(result.json['data']) == NUM_RECORDS
    assert result.json['last_id'] == result.json['data'][-1]['id']


def test_user_get_list_nonint_parameter(base_url, populate_db):

    NUM_RECORDS = 3
    populate_db(num_entries_to_insert=NUM_RECORDS)
    params = {'last_id': 'word'}

    result = requests.get(base_url, params=params)

    assert result.status_code == 422

def test_users_get_single_item(base_url):

    result = requests.get(base_url + '/1')
    assert result.status_code == 200


def test_users_get_single_item_not_found(base_url):

    result = requests.get(base_url + '/927402')
    assert result.status_code == 404

def test_users_put_not_found(base_url):

    user_to_update = {
        "title": "Return of the Jedi",
        "year": 1985,
        "description": "Ewoks gallore"
    }

    result = requests.put(base_url + '/927402', json=user_to_update)
    assert result.status_code == 500
    #TODO returns 500? 404?

def test_users_delete_not_found(base_url):
    #TODO returns 200?
    result = requests.delete(base_url + '/927402')
    assert result.status_code == 404


def test_user_crud_lifecycle(base_url):
    #TODO TypeError: 'instancemethod' - requests0?

    user_to_test = {
            "name": "Ervin Howell",
            "username": "Antonette",
            "email": "Shanna@melissa.tv"
            }

    # POST
    result = requests.post(base_url, json=user_to_test)

    assert result.status_code == 201
    assert 'location' in result.headers

    created_id = result.headers['location'].split('/')[-1]

    # GET
    result = requests.get(base_url + created_id)
    payload = result.json['data']
    payload.pop('id')

    assert result.status_code == 200
    assert payload == user_to_test

    # PUT
    user_to_test['username'] = "Antonette"

    result = base_url.simulate_put('/{}'.format(created_id), json=user_to_test)

    assert result.status == 200

    # GET
    result = base_url.simulate_get('/{}'.format(created_id))
    payload = result.json['data']
    payload.pop('id')

    assert result.status_code == 200
    assert payload == user_to_test

    # DELETE
    result = base_url.simulate_delete('/{}'.format(created_id))

    assert result.status_code == 204
