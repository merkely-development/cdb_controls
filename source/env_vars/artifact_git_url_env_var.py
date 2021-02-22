from env_vars import CompoundEnvVar, DynamicEnvVar

NAME = "MERKELY_ARTIFACT_GIT_URL"
NOTE = "The link to the source git commit this build was based on."


class ArtifactGitUrlEnvVar(DynamicEnvVar):

    def __init__(self, env):
        super().__init__(env, NAME, NOTE)

    @property
    def _ci_env_vars(self):
        return {
            'bitbucket': CompoundEnvVar(self._env, self.name,
                'https://bitbucket.org',
                '/',
                '${BITBUCKET_WORKSPACE}',
                '/',
                '${BITBUCKET_REPO_SLUG}',
                '/commits/',
                '${BITBUCKET_COMMIT}'
            ),
            'github': CompoundEnvVar(self._env, self.name,
                '${GITHUB_SERVER_URL}',
                '/',
                '${GITHUB_REPOSITORY}',
                '/commits/',
                '${GITHUB_SHA}'
            )
        }