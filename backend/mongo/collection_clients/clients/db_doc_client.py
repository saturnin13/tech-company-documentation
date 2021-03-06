from mongo.collection_clients.abstract_db_collection_client import AbstractDbCollectionClient
from mongo.constants.db_update_actions import DbUpdateActions
from mongo.models.db_doc_model import DbDocModel


class DbDocClient(AbstractDbCollectionClient):
    """
    A client for the database document collection.
    """

    def __init__(self):
        super().__init__('document', DbDocModel)

    def find(self, github_account_login):
        return self._find(
            DbDocModel(
                github_account_login=github_account_login
            )
        )

    def find_one(self, github_account_login, name):
        return self._find_one(
            DbDocModel(
                github_account_login=github_account_login,
                name=name
            )
        )

    def update(self, id, github_account_login, path, start_line, end_line, is_deleted):
        return self._update_one(
            DbDocModel(
                github_account_login=github_account_login,
                refs=[
                    DbDocModel.DbRefModel(
                        id=id
                    )
                ]
            ),
            DbDocModel(
                refs=[
                    DbDocModel.DbRefModel(
                        path=path,
                        start_line=start_line,
                        end_line=end_line,
                        is_deleted=is_deleted
                    )
                ]
            ),
            DbUpdateActions.SET_ACTION
        )

    def insert_one(self, json_doc):
        return self._insert_one(
            DbDocModel.from_json(json_doc)
        )
