from inference.worker import process_job


def test_worker_placeholder_contract():
    assert process_job('{"jobId":"placeholder"}')['status'] == 'placeholder'
