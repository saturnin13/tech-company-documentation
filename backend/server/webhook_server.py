import json

from flask import jsonify, request, abort, Blueprint

from github_interface.constants.github_api_fields import GithubApiFields
from github_interface.constants.github_api_values import GithubApiValues
from github_interface.constants.github_event_values import GithubEventValues
from github_interface.security.signature_validator import SignatureValidator
from tools import logger
from utils.global_constant import GlobalConst
from webhook_endpoints.installation_request_handler import InstallationRequestHandler
from webhook_endpoints.push_and_pr_request_handler import PushAndPRRequestHandler

webhook_server = Blueprint('webhook_server', __name__)

# TODO: create an interface for each different options that the class inherits and then add an enact to execute it
@webhook_server.route("/webhook_handler", methods=['POST'])
def webhook_handler():
    data = json.loads(request.data.decode("utf-8"))
    logger.get_logger().info("Webhook has been called for %s with action %s", request.headers['x-github-event'],
                             data[GithubApiFields.ACTION] if GithubApiFields.ACTION in data else "")

    if not __signature_valid():
        abort(401)

    event_type = request.headers['x-github-event']

    if __is_push_event(event_type):
        request_handler = PushAndPRRequestHandler(data[GithubApiFields.REPOSITORY][GithubApiFields.OWNER][GithubApiFields.LOGIN], data[GithubApiFields.REPOSITORY][GithubApiFields.NAME])
        if __is_branch_master(data[GithubApiFields.REF]):
            request_handler.enact_push_event()

    elif __is_pull_request_opened_event(event_type, data):
        request_handler = PushAndPRRequestHandler(data[GithubApiFields.REPOSITORY][GithubApiFields.OWNER][GithubApiFields.LOGIN], data[GithubApiFields.REPOSITORY][GithubApiFields.NAME])
        request_handler.enact_pull_request_opened_event(data[GithubApiFields.NUMBER])

    elif __is_installation_created_event(event_type, data):
        request_handler = InstallationRequestHandler(data[GithubApiFields.INSTALLATION][GithubApiFields.ACCOUNT][GithubApiFields.LOGIN])
        request_handler.enact_installation_created_event([data_repo[GithubApiFields.NAME] for data_repo in data[GithubApiFields.REPOSITORIES]], data[GithubApiFields.INSTALLATION][GithubApiFields.ID])

    elif __is_installation_deleted_event(event_type, data):
        request_handler = InstallationRequestHandler(data[GithubApiFields.INSTALLATION][GithubApiFields.ACCOUNT][GithubApiFields.LOGIN])
        request_handler.enact_installation_deleted_event()

    return jsonify({})

def __is_push_event(event_type):
    return event_type == GithubEventValues.PUSH

def __is_pull_request_opened_event(event_type, data):
    return event_type == GithubEventValues.PULL_REQUEST and data[GithubApiFields.ACTION] == GithubApiValues.OPENED

def __is_installation_created_event(event_type, data):
    return event_type == GithubEventValues.INSTALLATION and data[GithubApiFields.ACTION] == GithubApiValues.CREATED

def __is_installation_deleted_event(event_type, data):
    return event_type == GithubEventValues.INSTALLATION and data[GithubApiFields.ACTION] == GithubApiValues.DELETED

def manually_update_db(github_account_login, repo_name):
    PushAndPRRequestHandler(github_account_login, repo_name).enact_push_event()

def __signature_valid():
    signature = request.headers['X-Hub-Signature']
    body = request.get_data()
    return SignatureValidator().verify_signature(signature, body, GlobalConst.GITHUB_WEBHOOK_SECRET)

def __is_branch_master(ref):
    return ref[ref.rfind('/') + 1:] == "master"
