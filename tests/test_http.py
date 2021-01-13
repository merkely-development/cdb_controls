from cdb.http import http_put_payload, http_post_payload
from cdb.dry_run import cdb_dry_run


def test_put_dry_run_doesnt_call(mocker, capsys):
    requests = mocker.patch('cdb.http.req')
    with cdb_dry_run():
        http_put_payload("https://www.example.com", {}, "")
    requests.put.assert_not_called()
    read_stdout_stderr_to_keep_test_output_clean(capsys)


def test_post_dry_run_doesnt_call(mocker, capsys):
    requests = mocker.patch('cdb.http.req')
    with cdb_dry_run():
        http_post_payload("https://www.example.com", {}, "")
    requests.post.assert_not_called()
    read_stdout_stderr_to_keep_test_output_clean(capsys)


def read_stdout_stderr_to_keep_test_output_clean(capsys):
    capsys.readouterr()
