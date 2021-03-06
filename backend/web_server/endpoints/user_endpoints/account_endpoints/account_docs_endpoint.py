from marshmallow import Schema, fields

from mongo.collection_clients.clients.db_doc_client import DbDocClient
from mongo.constants.model_fields import ModelFields
from web_server.endpoints.user_endpoints.account_endpoints.abstract_user_account_endpoint import AbstractAccountEndpoint


# TODO: Add input validation and input sanitising
class AccountDocsEndpoint(AbstractAccountEndpoint):

    def __init__(self):
        super().__init__()
        self._get_output_schema_instance = Schema.from_dict({
            ModelFields.NAME: fields.Str(required=True)
        })(many=True)

    def get(self, github_account_login):
        docs = DbDocClient().find(github_account_login)

        return self._create_validated_response(docs)
