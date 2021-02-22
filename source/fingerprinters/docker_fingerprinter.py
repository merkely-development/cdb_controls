from errors import ChangeError
from fingerprinters import Fingerprinter
import docker

PROTOCOL = 'docker://'

NOTES = " ".join([
    f'The string `{PROTOCOL}` followed by the name+tag of the docker image to fingerprint.',
    'The docker socket must be volume-mounted.',
    'The image must have been pushed to a registry.'
])

EXAMPLE = "\n".join([
    'docker run ... \\',
    f'    --env MERKELY_FINGERPRINT=”{PROTOCOL}${{YOUR_DOCKER_IMAGE_AND_TAG}}" \\',
    '    --volume /var/run/docker.sock:/var/run/docker.sock \\',
    '    ...',
])


class DockerFingerprinter(Fingerprinter):

    @property
    def notes(self):
        return NOTES

    @property
    def example(self):
        return EXAMPLE

    def handles_protocol(self, string):
        return string.startswith(PROTOCOL)

    def artifact_basename(self, string):
        return self.artifact_name(string)

    def artifact_name(self, string):
        assert self.handles_protocol(string)
        result = string[len(PROTOCOL):]
        if result == "":
            raise ChangeError(f"Empty {PROTOCOL} fingerprint")
        return result

    def sha(self, string):
        assert self.handles_protocol(string)
        image_name = self.artifact_name(string)
        # Mocked in /tests/unit/utils/mock_docker_fingerprinter.py
        # docker is a Python package installed in requirements.txt
        client = docker.from_env()
        image = client.images.get(image_name)
        return image.attrs["RepoDigests"][0].split(":")[1]
        # If the image name is incorrect you get an
        # exception and a diagnostic on the terminal.
        # For example, see
        # https://github.com/merkely-development/loan-calculator/runs/1903030144?check_suite_focus=true
