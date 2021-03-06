from pymongo import ReturnDocument

from mongo.collection_clients.abstract_db_collection_client import AbstractDbCollectionClient
from mongo.constants.db_update_actions import DbUpdateActions
from mongo.models.db_counter_model import DbCounterModel


class DbCounterClient(AbstractDbCollectionClient):
    """
    A client for the database counter collection.
    """

    # Id value
    COUNTER_ACCOUNT_INSTALLATION_ID_FIELD = "installation_id_counter"

    def __init__(self):
        super().__init__('counter', DbCounterModel)

    def init(self):
        """
        Initialise the counter in the databsae.
        """

        if len(self._find_all()) == 0:
            self._insert_one(
                DbCounterModel(
                    id=DbCounterClient.COUNTER_ACCOUNT_INSTALLATION_ID_FIELD,
                    counter=0
                )
            )

    def get_next_account_installation_id(self):
        """
        Increment the account installation id.
        """

        db_counter = self._find_one_and_update(
            DbCounterModel(
                id=DbCounterClient.COUNTER_ACCOUNT_INSTALLATION_ID_FIELD
            ),
            DbCounterModel(
                counter=1
            ),
            DbUpdateActions.INC_ACTION,
            ReturnDocument.AFTER
        )

        return db_counter[DbCounterModel.COUNTER_FIELD]


# Always init the model before using it
DbCounterClient().init()
