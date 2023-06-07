from datetime import datetime


def test_salary_me(active_client, salaries_in_db):
    response = active_client.get('/v1/salary/me')
    assert response.status_code == 200, 'Неверный код ответа'

    data = response.json()
    salary = salaries_in_db[0][1]

    salary.pop('_sa_instance_state')
    salary['next_increase_date'] = datetime.strftime(
        salary.get('next_increase_date'), '%Y-%m-%dT%H:%M:%S')
    expected_keys = sorted(list(salary.keys()))
    response_keys = sorted(list(data.keys()))
    assert expected_keys == response_keys, (
        'ключи в отчете не такие, как ожидались')

    for key in expected_keys:
        assert salary[key] == data[key], (
            f'{salary["employee_id"]}, {key}: значение в ответе '
            'отличается от ожидаемого')


def test_salary_me_no_access(test_client, salaries_in_db):
    response = test_client.get('/v1/salary/me')
    data = response.json()
    assert response.status_code == 403, 'Неверный код ответа'
    assert list(data.keys()) == ['detail'], 'Неверный ключ в ответе'


def test_salary_get(superuser_client, salaries_in_db):
    response = superuser_client.get('/v1/salary/')
    assert response.status_code == 200, 'Неверный код ответа'

    data = response.json()
    salary_list = salaries_in_db[0]
    assert len(data) == len(salary_list), (
        'Число записей в ответе отличается от ожидаемого')

    for idx, salary in enumerate(salary_list):
        salary.pop('_sa_instance_state')
        salary['next_increase_date'] = datetime.strftime(
            salary.get('next_increase_date'), '%Y-%m-%dT%H:%M:%S')
        expected_keys = sorted(list(salary.keys()))
        response_keys = sorted(list(data[idx].keys()))
        assert expected_keys == response_keys, (
            'ключи в отчете не такие, как ожидались')

        for key in expected_keys:
            assert salary[key] == data[idx][key], (
                f'{salary["employee_id"]}, {key}: значение в ответе '
                'отличается от ожидаемого')


def test_salary_get_post_no_access(active_client, test_client,
                                   salaries_in_db):
    new_salary = {
        'salary': 50000,
        'employee_id': 3,
        'next_increase_date': '2023-10-01T00:00:00',
    }
    for client in (active_client, test_client):
        response_get = client.get('/v1/salary/')
        response_post = client.post('/v1/salary/', json=new_salary)
        data_get = response_get.json()
        data_post = response_post.json()
        assert response_get.status_code == 403, 'GET: Неверный код ответа'
        assert response_post.status_code == 403, 'POST: Неверный код ответа'
        assert list(data_get.keys()) == ['detail'], (
            'GET:Неверный ключ в ответе')
        assert list(data_post.keys()) == ['detail'], (
            'POST:Неверный ключ в ответе')


def test_salary_post_correct_data(superuser_client, salaries_in_db):
    new_salary = {
        'salary': 50000,
        'employee_id': 3,
        'next_increase_date': '2023-10-01T00:00:00',
    }
    response = superuser_client.post(
        '/v1/salary/',
        json=new_salary)
    data = response.json()

    assert response.status_code == 200, 'Неверный код ответа'
    assert data.get('id') is not None, 'В ответе нет ключа `id`'

    data.pop('id')
    expected_keys = sorted(list(new_salary.keys()))
    data_keys = sorted(list(data.keys()))
    assert expected_keys == data_keys, 'Неверные ключи в ответе'
    for key in expected_keys:
        assert data[key] == new_salary[key], (
            'Неверные значения ключей в ответе')


def test_users_post_incorrect_data(superuser_client, salaries_in_db):
    new_salary = {
        'salary': 50000,
        'employee_id': 3,
        'next_increase_date': '2023-10-01T00:00:00',
    }
    required_keys = ['salary', 'employee_id', 'next_increase_date']
    for key in required_keys:
        salary = new_salary.copy()
        salary.pop(key)
        response = superuser_client.post(
            '/v1/salary/',
            json=salary)
        data = response.json()
        assert response.status_code == 422, 'Неверный код ответа'
        assert list(data.keys()) == ['detail'], 'Неверные ключи в ответе'
