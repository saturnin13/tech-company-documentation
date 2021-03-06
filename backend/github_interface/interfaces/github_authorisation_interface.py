import requests

from github_interface.interfaces.github_facade.raw_github_facade import RawGithubFacade
from tools import logger
from utils.secret_constant import SecretConstant


class GithubAuthorisationInterface:
    """
    A class to handle all the github authorisation and authentification requests.
    """

    @staticmethod
    def request_user_token(client_id, client_secret, code, redirect_uri):
        logger.get_logger().info("Requesting the user token")

        params = {
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "redirect_uri": redirect_uri
        }
        response = requests.get(url="https://github.com/login/oauth/access_token", params=params)
        decoded_content = response.content.decode("utf-8")
        user_token = decoded_content[decoded_content.find("access_token=") + 13: decoded_content.find("&")]

        return user_token

    @staticmethod
    def request_user_login(user_token):
        logger.get_logger().info("Requesting the user login")

        user = RawGithubFacade.UserFacade(user_token).get_user()

        return user.login

    @staticmethod
    def request_installation_token(installation_id, private_key):

        installation_token = RawGithubFacade.get_access_token(
            str(SecretConstant.GITHUB_APP_IDENTIFIER),
            private_key,
            installation_id
        )

        return installation_token.token, installation_token.expires_at
