from commands import command_processor
from tests.utils import *


def test_file_at_root(capsys):
    commit = "abc50c8a53f79974d615df335669b59fb56a4ed3"
    digest = "ccdd89ccdc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc"
    ev = log_artifact_env(commit)
    ev["MERKELY_FINGERPRINT"] = "file://coverage.txt"

    with ScopedEnvVars({**DRY_RUN, **ev}) as env, scoped_merkelypipe_json():
        with ScopedFileCopier("/app/tests/data/coverage.txt", "/coverage.txt"):
            context = make_context(env)
            context.sha_digest_for_file = lambda _filename: digest
            status_code = command_processor.execute(context)

    assert status_code == 0
    verify_payload_and_url(capsys)


def test_file_not_at_root(capsys):
    commit = "abc50c8a53f79974d615df335669b59fb56a4444"
    digest = "ccdd89ccdc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f5115"
    ev = log_artifact_env(commit)
    ev["MERKELY_FINGERPRINT"] = "file://app/tests/data/coverage.txt"

    with ScopedEnvVars({**DRY_RUN, **ev}) as env, scoped_merkelypipe_json():
        context = make_context(env)
        context.sha_digest_for_file = lambda _filename: digest
        status_code = command_processor.execute(context)

    assert status_code == 0
    verify_payload_and_url(capsys)


def test_docker_image(capsys):
    commit = "ddc50c8a53f79974d615df335669b59fb56a4ed3"
    digest = "ddee5566dc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc"
    ev = log_artifact_env(commit)
    ev["MERKELY_FINGERPRINT"] = "docker://acme/road-runner:6.8"

    with ScopedEnvVars({**DRY_RUN, **ev}) as env, scoped_merkelypipe_json():
        context = make_context(env)
        context.sha_digest_for_docker_image = lambda _image_name: digest
        status_code = command_processor.execute(context)

    assert status_code == 0
    verify_payload_and_url(capsys)


def test_sha256_file(capsys):
    commit = "ddc50c8a53f79974d615df335669b59fb56a4ed3"
    digest = "ddee5566dc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc"
    ev = log_artifact_env(commit)
    ev["MERKELY_FINGERPRINT"] = f"sha256://{digest}"
    ev["MERKELY_ARTIFACT"] = "file://app/tests/data/coverage.txt"

    with ScopedEnvVars({**DRY_RUN, **ev}) as env, scoped_merkelypipe_json():
        context = make_context(env)
        status_code = command_processor.execute(context)

    assert status_code == 0
    verify_payload_and_url(capsys)


def test_MERKELY_CI_BUILD_NUMBER_missing(capsys):
    ev = log_artifact_env(any_commit())
    ev.pop("MERKELY_CI_BUILD_NUMBER")

    with ScopedEnvVars({**DRY_RUN, **ev}) as env, scoped_merkelypipe_json():
        context = make_context(env)
        status_code = command_processor.execute(context)

    assert status_code != 0
    verify_approval(capsys)


def test_MERKELY_ARTIFACT_GIT_COMMIT_missing(capsys):
    ev = log_artifact_env(any_commit())
    ev.pop("MERKELY_ARTIFACT_GIT_COMMIT")

    with ScopedEnvVars({**DRY_RUN, **ev}) as env, scoped_merkelypipe_json():
        context = make_context(env)
        status_code = command_processor.execute(context)

    assert status_code != 0
    verify_approval(capsys)


def log_artifact_env(commit):
    return {
        "MERKELY_COMMAND": "log_artifact",
        "MERKELY_API_TOKEN": "MY_SUPER_SECRET_API_TOKEN",
        "MERKELY_FINGERPRINT": "file://coverage.txt",  # at root
        "MERKELY_HOST": "https://test.merkely.com",
        "MERKELY_CI_BUILD_URL": "https://gitlab/build/1456",
        "MERKELY_CI_BUILD_NUMBER": "23",
        "MERKELY_ARTIFACT_GIT_URL": "http://github/me/project/commit/" + commit,
        "MERKELY_ARTIFACT_GIT_COMMIT": commit,
        "MERKELY_IS_COMPLIANT": "TRUE"
    }


def any_commit():
    return "abc50c8a53f79974d615df335669b59fb56a4ed3"


def scoped_merkelypipe_json():
    return ScopedFileCopier("/app/tests/data/Merkelypipe.json", "/Merkelypipe.json")