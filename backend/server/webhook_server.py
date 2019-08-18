import json

from flask import jsonify, request, abort, Blueprint

from github_interface.authorisation_interface import GithubAuthorisationInterface
from tools import logger
from utils.constants import GITHUB_WEBHOOK_SECRET
from webhook.installation_request_handler import InstallationRequestHandler
from webhook.push_and_pr_request_handler import PushAndPRRequestHandler

webhook_server = Blueprint('webhook_server', __name__)


@webhook_server.route("/webhook_handler", methods=['POST'])
def webhook_handler():
    logger.get_logger().info("Webhook has been called for %s", request.headers['x-github-event'])

    if not __signature_valid():
        abort(401)

    event_type = request.headers['x-github-event']
    data = json.loads(request.data.decode("utf-8"))

    if event_type == "push":
        request_handler = PushAndPRRequestHandler(data["repository"]["owner"]["login"], data["repository"]["full_name"])
        if __is_branch_master(data["ref"]):
            request_handler.enact_push_event()

    elif event_type == "pull_request" and data["action"] == "opened":
        request_handler = PushAndPRRequestHandler(data["repository"]["owner"]["login"], data["repository"]["full_name"])
        request_handler.enact_pull_request_opened_event(data["number"])

    elif event_type == "installation" and data["action"] == "deleted":
        request_handler = InstallationRequestHandler(data["installation"]["account"]["login"])
        request_handler.enact_installation_deleted_event()

    response = jsonify({})
    return response


def manually_update_db(organisation_login, repo_full_name):
    PushAndPRRequestHandler(organisation_login, repo_full_name).enact_push_event()


def __signature_valid():
    signature = request.headers['X-Hub-Signature']
    body = request.get_data()
    return GithubAuthorisationInterface.verify_signature(signature, body, GITHUB_WEBHOOK_SECRET)


def __is_branch_master(ref):
    return ref[ref.rfind('/') + 1:] == "master"
