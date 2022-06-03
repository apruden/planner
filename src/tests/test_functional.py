def test_get_workers_empty(client):
    workers = client.get('/workers').get_json()

    assert workers == []

def test_create_worker(client):
    client.post('/workers', json={'name': 'foo'})
    workers = client.get('/workers').get_json()

    assert workers == [{'id': 1, 'name': 'foo'}]

def test_create_worker_allocation(client):
    client.post('/workers', json={'name': 'foo'})
    client.post('/workers/1/allocations', json={'date': '2022-10-10', 'shift': 'DAY'})
    allocations = client.get('/workers/1/allocations').get_json()

    assert allocations == [{'id': 1, 'date': '2022-10-10', 'shift': 'DAY', 'worker': {'id': 1, 'name': 'foo'}}]

