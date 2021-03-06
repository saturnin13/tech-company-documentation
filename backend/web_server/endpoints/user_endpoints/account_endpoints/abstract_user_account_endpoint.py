from functools import wraps

from flask import session
from flask_restful import abort

from github_interface.interfaces.web_server_github_interface import WebServerGithubInterface
from tools import logger
from web_server.endpoints.abstract_endpoint import AbstractEndpoint
from web_server.endpoints.user_endpoints.abstract_user_endpoint import AbstractUserEndpoint


class AbstractAccountEndpoint(AbstractUserEndpoint):
    """
    Abstract endpoint for handling user accessing of a specific documentation account. It verifies that the user has
    access to this specific account. It inherits the AbstractUserEndpoint and therefore it also verifies that the user
    is authenticated.
    """

    def __init__(self):
        super(AbstractAccountEndpoint, self).__init__()
        self.method_decorators = [AbstractAccountEndpoint.github_account_access_validation_required] + self.method_decorators

    @staticmethod
    def github_account_access_validation_required(f):

        @wraps(f)
        def wrap(*args, **kwargs):

            if not AbstractAccountEndpoint.__can_user_access_github_account(kwargs["github_account_login"]):
                logger.get_logger().error('User is not authorised to access this installation for %s', kwargs["github_account_login"])
                return abort(403, message="Unauthorised access to this account by the user")

            return f(*args, **kwargs)

        return wrap

    @staticmethod
    def __can_user_access_github_account(github_account_login):
        user_installations = WebServerGithubInterface(
            session[AbstractEndpoint.COOKIE_USER_LOGIN_FIELD]).request_installations()

        for installation in user_installations:

            if github_account_login == installation.github_account_login:
                return True

        return False
