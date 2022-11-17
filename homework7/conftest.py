import os
import signal
import subprocess
import time
from copy import copy
import pytest
import settings
import requests
from requests import ConnectionError

from client import APIClient

repo_root = os.path.abspath(os.path.join(__file__, os.path.pardir))


@pytest.fixture(scope='session')
def api_log_client():
    logs_path = os.path.join(repo_root, 'tmp', 'logs')
    return APIClient(log_file=logs_path)

def wait_ready(host, port):
    started = False
    st = time.time()
    while time.time() - st <= 5:
        try:
            requests.get(f'http://{host}:{port}')
            started = True
            break
        except ConnectionError:
            pass
    if not started:
        raise RuntimeError('App didn\'t started in 5s!')


def pytest_configure(config):
    if not hasattr(config, 'workerinput'):
        app_path = os.path.join(repo_root, 'application', 'app_fast_api.py')
        env = copy(os.environ)
        env.update({'APP_HOST': settings.APP_HOST, 'APP_PORT': settings.APP_PORT})
        env.update({'STUB_HOST': settings.STUB_HOST, 'STUB_PORT': settings.STUB_PORT})
        app_stderr_path = os.path.join(repo_root, 'tmp', 'app_stderr')
        app_stdout_path = os.path.join(repo_root, 'tmp', 'app_stdout')
        app_stderr = open(app_stderr_path, 'w')
        app_stdout = open(app_stdout_path, 'w')
        proc = subprocess.Popen(['python3', app_path], env=env,
                                stderr=app_stderr, stdout=app_stdout)
        config.proc = proc
        config.app_stderr = app_stderr
        config.app_stdout = app_stdout
        wait_ready(settings.APP_HOST, settings.APP_PORT)

        # stub config

        stub_path = os.path.join(repo_root, 'stub', 'stub.py')

        stub_stderr_path = os.path.join(repo_root, 'tmp', 'stub_stderr')
        stub_stdout_path = os.path.join(repo_root, 'tmp', 'stub_stdout')
        stub_stderr = open(stub_stderr_path, 'w')
        stub_stdout = open(stub_stdout_path, 'w')

        stub_proc = subprocess.Popen(['python3', stub_path], env=env,
                                     stderr=stub_stderr, stdout=stub_stdout)
        config.stub_proc = stub_proc
        config.stub_stderr = stub_stderr
        config.stub_stdout = stub_stdout
        wait_ready(settings.STUB_HOST, settings.STUB_PORT)


def pytest_unconfigure(config):
    config.proc.send_signal(signal.SIGINT)
    exit_code = config.proc.wait()
    assert exit_code == 0
    config.app_stderr.close()
    config.app_stdout.close()

    config.stub_proc.send_signal(signal.SIGINT)
    exit_code = config.stub_proc.wait()
    assert exit_code == 0
    config.stub_stderr.close()
    config.stub_stdout.close()
