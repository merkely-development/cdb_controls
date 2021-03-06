from errors import ChangeError
from env_vars import CompoundEnvVar, CiEnvVar
from pytest import raises

NAME = "MERKELY_ARTIFACT_GIT_URL"


def test_original_env_var_is_used_in_error_messages():
    ev = {}
    target = CompoundEnvVar(ev, NAME, 'abc')
    assert target.name == NAME


def test_plain_strings_remain_unchanged():
    ev = {}
    target = CompoundEnvVar(ev, NAME, 'abc')
    assert target.string == 'abc'


def test_plain_string_are_concatenated():
    ev = {}
    target = CompoundEnvVar(ev, NAME, 'abc', '/', 'wibble.json')
    assert target.string == 'abc/wibble.json'


def test_plain_string_is_not_expanded():
    ev = {'NOT_AN_ENV_VAR': 'hello world'}
    target = CompoundEnvVar(ev, NAME, 'NOT_AN_ENV_VAR')
    assert target.value == 'NOT_AN_ENV_VAR'


def test_ci_env_var_string_is_expanded():
    ev = {'SOME_ENV_VAR': 'hello world'}
    target = CompoundEnvVar(ev, NAME, CiEnvVar('SOME_ENV_VAR'))
    assert target.value == 'hello world'


def test_expansion_of_ci_env_var_not_set_raises():
    ev = {}
    not_set = 'SOME_ENV_VAR'
    target = CompoundEnvVar(ev, NAME, '/path/', CiEnvVar(not_set))
    with raises(ChangeError) as exc:
        target.value

    assert str(exc.value) == \
        f"environment-variable {NAME} defaults to `{target.string}` " \
        f"but `{not_set}` is not set."


def test_ci_env_var_value_class():
    ev = {}
    part = CiEnvVar('WIBBLE')
    target = CompoundEnvVar(ev, NAME, part)
    assert target.string == "${WIBBLE}"