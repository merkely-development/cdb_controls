from cdb.create_approval import create_approval

from tests.cdb_dry_run import cdb_dry_run
from tests.test_git import TEST_REPO_ROOT
from tests.verify_approval import verify_approval


def test_put_approval(capsys):
    env = {
        "CDB_ARTIFACT_SHA": "1234",
        "CDB_BASE_SRC_COMMITISH": "production",
        "CDB_TARGET_SRC_COMMITISH": "master",
        "CDB_DESCRIPTION": "Description",
        "CDB_IS_APPROVED_EXTERNALLY": "FALSE",
        "CDB_SRC_REPO_ROOT": TEST_REPO_ROOT,
    }

    with cdb_dry_run():
        create_approval("integration_tests/test-pipefile.json", env)

    verify_approval(capsys, ["out", "err"])
