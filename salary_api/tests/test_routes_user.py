async def test_users_signin(superuser_client, create_users):
    response = superuser_client.post(
        '/v1/user/signin',
        headers={
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'},
        data=('grant_type=&username=User1&password=testpassword123'
              '&scope=&client_id=&client_secret='))
    data = response.json()
    keys = ['access_token', 'token_type']
    assert response.status_code == 200, 'Неверный код ответа'
    assert sorted(list(data.keys())) == keys, 'Неверные ключи в ответе'


def test_users_singin_invalid_pass(superuser_client, create_users):
    response = superuser_client.post(
        '/v1/user/signin',
        headers={
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'},
        data=('grant_type=&username=User1&password=testpassword124'
              '&scope=&client_id=&client_secret='))
    assert response.status_code == 401, 'Неверный код ответа'
    data = response.json()
    assert data == {'detail': 'Введен неверный пароль.'}, (
        'Неверное тело ответа')


def test_users_get(superuser_client, create_users):
    response = superuser_client.get('/v1/user/')
    assert response.status_code == 200, 'Неверный код ответа'
    data = response.json()
    user_num = len(create_users.values())

    assert len(data) == user_num, f'В ответе должно быть записей: {user_num}'
    for idx, item in enumerate(create_users.values()):
        user = item[0].__dict__.copy()
        user.pop('_sa_instance_state')
        user.pop('password')
        expected_keys = sorted(list(user.keys()))
        response_keys = sorted(list(data[idx].keys()))
        assert expected_keys == response_keys, (
            'ключи в отете не такие, как ожидались')
        for key in expected_keys:
            assert user[key] == data[idx][key], (
                f'{user["username"]}, {key}: значение в ответе '
                'отличается от ожидаемого')


def test_users_get_post_no_access(test_client, active_client, create_users):
    new_user = {
        'username': 'User1001',
        'password': 'Testpass125',
        'name': 'Виктор1',
        'surname': 'Тестовый1001',
        'job_title': 'Работник1001',
    }
    for client in (active_client, test_client):

        response_get = client.get('/v1/user/')
        response_post = client.post('/v1/user/', json=new_user)
        data_get = response_get.json()
        data_post = response_post.json()
        assert response_get.status_code == 403, 'GET: Неверный код ответа'
        assert response_post.status_code == 403, 'POST: Неверный код ответа'
        assert data_get == {'detail': 'Недостаточно прав для операции'}, (
            'GET:Неверное тело ответа')
        assert data_post == {'detail': 'Недостаточно прав для операции'}, (
            'POST:Неверное тело ответа')


def test_users_post_correct_data(superuser_client, create_users):
    new_user1 = {
        'username': 'User1000',
        'password': 'Testpass124',
        'name': 'Виктор',
        'surname': 'Тестовый1000',
        'job_title': 'Работник1000',
        'is_superuser': True,
        'is_active': True
    }
    new_user2 = {
        'username': 'User1001',
        'password': 'Testpass125',
        'name': 'Виктор1',
        'surname': 'Тестовый1001',
        'job_title': 'Работник1001',
    }
    for user in (new_user1, new_user2):
        response = superuser_client.post(
            '/v1/user/',
            json=user)
        data = response.json()

        assert response.status_code == 200, 'Неверный код ответа'
        assert data.get('id') is not None, 'В ответе нет ключа `id`'

        data.pop('id')
        user.pop('password')
        user['is_superuser'] = user.get('is_superuser', False)
        user['is_active'] = user.get('is_active', True)

        expected_keys = sorted(list(user.keys()))
        data_keys = sorted(list(data.keys()))
        assert expected_keys == data_keys, 'Неверные ключи в ответе'
        for key in expected_keys:
            assert data[key] == user[key], 'Неверные значения ключей в ответе'


def test_users_post_incorrect_data(superuser_client, create_users):
    new_user = {
        'username': 'User1001',
        'password': 'Testpass125',
        'name': 'Виктор1',
        'surname': 'Тестовый1001',
        'job_title': 'Работник1001',
    }
    required_keys = ['username', 'password', 'name', 'surname', 'job_title']
    for key in required_keys:
        user = new_user.copy()
        user.pop(key)
        response = superuser_client.post(
            '/v1/user/',
            json=user)
        data = response.json()
        assert response.status_code == 422, 'Неверный код ответа'
        assert list(data.keys()) == ['detail'], 'Неверные ключи в ответе'
