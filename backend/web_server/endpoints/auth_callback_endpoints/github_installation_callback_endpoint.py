from flask import session, request

from github_interface.interfaces.authenticated_github_interface import AuthenticatedGithubInterface
from mongo.constants.db_fields import ModelFields
from web_server.endpoints.abstract_endpoint import AbstractEndpoint


class GithubInstallationCallbackEndpoint(AbstractEndpoint):

    def post(self):
        super().post()
        installation_id = request.args['installation_id']
        setup_action = request.args['setup_action']

        installation = {}
        user_installations = AuthenticatedGithubInterface(session[AbstractEndpoint.USER_LOGIN_FIELD]).request_installations()
        for user_installation in user_installations:
            if int(user_installation.id) == int(installation_id):
                installation = user_installation

        return self._create_response({
            ModelFields.LOGIN: installation.github_account_login
        })
