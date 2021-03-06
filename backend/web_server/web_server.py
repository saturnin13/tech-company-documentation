from flask import Blueprint
from flask_restful import Api

from web_server.endpoints.auth_callback_endpoints.auth_github_callback_endpoint import AuthGithubCallbackEndpoint
from web_server.endpoints.auth_callback_endpoints.github_installation_callback_endpoint import \
    GithubInstallationCallbackEndpoint
from web_server.endpoints.user_endpoints.account_endpoints.account_docs_endpoint import AccountDocsEndpoint
from web_server.endpoints.user_endpoints.account_endpoints.account_fs_node_endpoint import AccountFSNodeEndpoint
from web_server.endpoints.user_endpoints.account_endpoints.account_lines_endpoint import AccountLinesEndpoint
from web_server.endpoints.user_endpoints.account_endpoints.account_render_endpoint import AccountRenderEndpoint
from web_server.endpoints.user_endpoints.account_endpoints.account_repos_endpoint import AccountReposEndpoint
from web_server.endpoints.user_endpoints.account_endpoints.account_save_endpoint import AccountSaveEndpoint
from web_server.endpoints.user_endpoints.user_endpoint import UserEndpoint
from web_server.endpoints.user_endpoints.user_installs_endpoint import UserInstallsEndpoint


# Routing for the webserver using the Flask restful library
web_server = Blueprint('web_server', __name__)
api = Api(web_server)

# Routing the authentication and authorisation endpoints
api.add_resource(AuthGithubCallbackEndpoint, "/auth/github/callback")
api.add_resource(GithubInstallationCallbackEndpoint, "/github_app_installation_callback")

# Routing the user endpoints
api.add_resource(UserEndpoint, "/user", "logout")
api.add_resource(UserInstallsEndpoint, "/installs")

# Routing the github account endpoints
api.add_resource(AccountReposEndpoint, "/<string:github_account_login>/repos")
api.add_resource(AccountFSNodeEndpoint, "/<string:github_account_login>/fs_nodes")
api.add_resource(AccountSaveEndpoint, "/<string:github_account_login>/save")
api.add_resource(AccountDocsEndpoint, "/<string:github_account_login>/docs")
api.add_resource(AccountRenderEndpoint, "/<string:github_account_login>/render")
api.add_resource(AccountLinesEndpoint, "/<string:github_account_login>/lines")
