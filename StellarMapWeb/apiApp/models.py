import datetime
import uuid

from cassandra.cqlengine import columns as cassandra_columns
from django_cassandra_engine.models import DjangoCassandraModel
from StellarMapWeb.settings.settings_base import CASSANDRA_DB_NAME

PENDING = 'pending'
IN_PROGRESS = 'in_progress'
COMPLETED = 'completed'
STATUS_CHOICES = (
    (PENDING, 'Pending'),
    (IN_PROGRESS, 'In Progress'),
    (COMPLETED, 'Completed'),
)

TESTNET = 'testnet'
PUBLIC = 'public'
NETWORK_CHOICES = (
    (TESTNET, 'testnet'),
    (PUBLIC, 'public'),
)

class BaseModel(DjangoCassandraModel):
    __keyspace__ = CASSANDRA_DB_NAME
    id = cassandra_columns.UUID(primary_key=True, default=uuid.uuid4)
    created_at = cassandra_columns.DateTime()
    updated_at = cassandra_columns.DateTime()

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.datetime.utcnow()
        self.updated_at = datetime.datetime.utcnow()
        return super().save(*args, **kwargs)
    
    class Meta:
        get_pk_field = "id"
        abstract = True

class StellarAccountInquiryHistory(DjangoCassandraModel):
    """
    A model for storing the history of user requests to examine a Stellar account.

    Attributes:
        stellar_account (str): a field that stores the address of the Stellar account
        network_name (str): a field that stores the network the Stellar account belongs to
        status (str): a field that stores the status of the request with a max length of 20 and a default value of 'pending'. The valid choices for the status field are 'pending', 'in_progress', and 'completed'.

    Note: 
        To prevent multiple requests for the same Stellar account, ask the user if they want to make a new request or retrieve data from previous requests for that Stellar account.
    """

    __keyspace__ = CASSANDRA_DB_NAME
    id = cassandra_columns.UUID(primary_key=True, default=uuid.uuid4)
    stellar_account = cassandra_columns.Text(primary_key=True, max_length=56)
    network_name = cassandra_columns.Text(primary_key=True, max_length=9)
    status = cassandra_columns.Text(max_length=63)
    created_at = cassandra_columns.DateTime(primary_key=True, clustering_order="DESC")
    updated_at = cassandra_columns.DateTime()

    def __str__(self):
        """ Method to display Stellar account, network and status in the admin django interface.
        """
        return 'Stellar Account: ' + self.stellar_account + ' | network: ' + self.network_name + ' | status: ' + self.status

    class Meta:
        get_pk_field = "id"
        db_table = 'stellar_account_inquiry_history'

class StellarAccountLineage(DjangoCassandraModel):
    """
    A model for storing detailed information about the lineage and creator accounts of the Stellar network.
    
    Attributes:
        account_active (str): a field that stores whether or not the Stellar account is active
        stellar_creator_account (str): a field that stores the address of the Stellar account creator
        stellar_account (str): a field that stores the address of the Stellar account
        stellar_account_created_at (datetime): a field that stores the date and time when the Stellar account was created
        network_name (str): a field that stores the network name
        home_domain (str): a field that stores the home domain
        xlm_balance (float): a field that stores the XLM balance of the Stellar account
        horizon_accounts_doc_api_href (str): a field that stores the horizon accounts doc api href
        horizon_accounts_operations_doc_api_href (str): a field that stores the horizon accounts operations doc api href
        horizon_accounts_effects_doc_api_href (str): a field that stores the horizon accounts effects doc api href
        stellar_expert_explorer_account_doc_api_href (str): a field that stores the Stellar expert explorer account doc api href
        status (str): a field that stores the status of the request with a default value of 'pending'. The valid choices for the status field are 'pending', 'in_progress', and 'completed'.
    """

    __keyspace__ = CASSANDRA_DB_NAME
    id = cassandra_columns.UUID(primary_key=True, default=uuid.uuid4)
    account_active = cassandra_columns.Text(max_length=30)
    stellar_creator_account = cassandra_columns.Text(max_length=56)
    stellar_account = cassandra_columns.Text(primary_key=True, max_length=56)
    stellar_account_created_at = cassandra_columns.DateTime()
    network_name = cassandra_columns.Text(primary_key=True, max_length=9)
    home_domain = cassandra_columns.Text(max_length=71)
    xlm_balance = cassandra_columns.Float()
    horizon_accounts_doc_api_href = cassandra_columns.Text() # "https://horizon.stellar.org/accounts/{stellar_account}"
    horizon_accounts_operations_doc_api_href = cassandra_columns.Text() # "https://horizon.stellar.org/operations/{stellar_account}"
    horizon_accounts_effects_doc_api_href = cassandra_columns.Text() # https://horizon.stellar.org/accounts/{stellar_account}/effects
    stellar_expert_explorer_account_doc_api_href = cassandra_columns.Text() # https://api.stellar.expert/explorer/{network_name}/account/{stellar_account}
    status = cassandra_columns.Text(max_length=63)
    created_at = cassandra_columns.DateTime(primary_key=True, clustering_order="DESC")
    updated_at = cassandra_columns.DateTime()

    def __str__(self):
        """ Method to display Stellar account, network and status in the admin django interface.
        """
        return 'Stellar Account: ' + self.stellar_account + ' | network: ' + self.network_name + ' | status: ' + self.status

    class Meta:
        get_pk_field = "id"


class ManagementCronHealthHistory(DjangoCassandraModel):
    """
    A model that holds information on the status of each cron job in the system.
    The initial status of each cron job is set to "HEALTHY". In case of errors,
    the status will be prefixed with "ERROR_". Before executing a cron job, the
    most recent record entry is checked to verify its status. If the status is
    not healthy, the cron job will not execute. This mechanism is in place to
    support the tenacity library, which implements exponential backoff in case
    of repeated errors and stops the cron job execution once the maximum number
    of retries is reached.

    Attributes:
        id (uuid.UUID): A unique identifier for the record, generated using uuid4 by default.
        cron_name (str): The name of the cron job. The max length is 71.
        status (str): The health status of the cron job. The default status is "HEALTHY", and if there is an error, it is prefixed with "ERROR_". The max length is 63.
        created_at (datetime.datetime): The creation time of the record.
        updated_at (datetime.datetime): The last update time of the record.
    """
    __keyspace__ = CASSANDRA_DB_NAME
    id = cassandra_columns.UUID(primary_key=True, default=uuid.uuid4)
    cron_name = cassandra_columns.Text(max_length=71)
    status = cassandra_columns.Text(max_length=63)
    reason = cassandra_columns.Text()
    created_at = cassandra_columns.DateTime()
    updated_at = cassandra_columns.DateTime()

    def __str__(self):
        """ Method to display cron name and status in the admin django interface.
        """
        return 'Cron Name: ' + self.cron_name + ' | Status: ' + self.status

    class Meta:
        get_pk_field = "id"


class ManagementCronHealth(DjangoCassandraModel):
    """
    A model that holds information on the status of each cron job in the system.
    The initial status of each cron job is set to "HEALTHY". In case of errors,
    the status will be prefixed with "ERROR_". Before executing a cron job, the
    most recent record entry is checked to verify its status. If the status is
    not healthy, the cron job will not execute. This mechanism is in place to
    support the tenacity library, which implements exponential backoff in case
    of repeated errors and stops the cron job execution once the maximum number
    of retries is reached.

    Note: 
        CQL to use order by DESC on created_at
        >>> CREATE TABLE management_cron_health (
        >>>     id UUID,
        >>>     cron_name text,
        >>>     status text,
        >>>     reason text,
        >>>     created_at timestamp,
        >>>     updated_at timestamp,
        >>>     PRIMARY KEY (id, cron_name, created_at)
        >>> ) WITH CLUSTERING ORDER BY (cron_name ASC, created_at DESC)


    Attributes:
        id (uuid.UUID): A unique identifier for the record, generated using uuid4 by default.
        cron_name (str): The name of the cron job. The max length is 71.
        status (str): The health status of the cron job. The default status is "HEALTHY", and if there is an error, it is prefixed with "ERROR_". The max length is 63.
        created_at (datetime.datetime): The creation time of the record.
        updated_at (datetime.datetime): The last update time of the record.
    """
    __keyspace__ = CASSANDRA_DB_NAME
    id = cassandra_columns.UUID(primary_key=True, default=uuid.uuid4)
    cron_name = cassandra_columns.Text(primary_key=True, max_length=71)
    status = cassandra_columns.Text(max_length=63)
    reason = cassandra_columns.Text()
    created_at = cassandra_columns.DateTime(primary_key=True, clustering_order="DESC")
    updated_at = cassandra_columns.DateTime()

    class Meta:
        db_table = 'management_cron_health'
        get_pk_field = "id"

    def __str__(self):
        """ Method to display cron name and status in the admin django interface.
        """
        return 'Cron Name: ' + self.cron_name + ' | Status: ' + self.status