from commands import DockerFingerprinter


class MockDockerFingerprinter(DockerFingerprinter):

    def __init__(self, image_name, digest):
        self._expected = image_name
        self._digest = digest
        self._called = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self._called:
            self._failed(["Expected call did not happen"])

    def _fingerprint(self, image_name):
        self._called = True
        if image_name == self._expected:
            return self._digest
        else:
            self._unmatched(image_name)

    def _unmatched(self, image_name):
        message = "\n".join([
            f"{self.__class__.__name__}._fingerprint(artifact_name)",
            "FAILED",
            f"Expected: artifact_name=={self._expected}",
            f"  Actual: artifact_name=={image_name}"
        ])
        raise RuntimeError(message)