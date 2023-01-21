import uuid
import datetime

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model as PythonCassandraModel
from django_cassandra_engine.models import DjangoCassandraModel

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

class BaseModel(DjangoCassandraModel, PythonCassandraModel):
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    created_at = columns.DateTime()
    updated_at = columns.DateTime()

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        return super().save(*args, **kwargs)
    
    class Meta:
        abstract = True

class StellarAccountInquiryHistory(BaseModel):
    """
    A model for storing the history of user requests to examine a Stellar account.

    Attributes:
        stellar_account (str): a field that stores the address of the Stellar account
        network_name (str): a field that stores the network the Stellar account belongs to
        status (str): a field that stores the status of the request with a max length of 20 and a default value of 'pending'. The valid choices for the status field are 'pending', 'in_progress', and 'completed'.

    Note: 
        To prevent multiple requests for the same Stellar account, ask the user if they want to make a new request or retrieve data from previous requests for that Stellar account.
    """

    stellar_account = columns.Text(max_length=56)
    network_name = columns.Text(max_length=9)
    status = columns.Text(max_length=20)

class StellarAccountLineage(BaseModel):
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

    account_active = columns.Text(max_length=30)
    stellar_creator_account = columns.Text(max_length=56)
    stellar_account = columns.Text(max_length=56)
    stellar_account_created_at = columns.DateTime()
    network_name = columns.Text(max_length=9)
    home_domain = columns.Text(max_length=71)
    xlm_balance = columns.Float()
    horizon_accounts_doc_api_href = columns.Text()
    horizon_accounts_operations_doc_api_href = columns.Text()
    horizon_accounts_effects_doc_api_href = columns.Text()
    stellar_expert_explorer_account_doc_api_href = columns.Text()
    status = columns.Text(max_length=36)

