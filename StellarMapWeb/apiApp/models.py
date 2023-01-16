import uuid
from datetime import datetime

from cassandra.cqlengine import columns
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

class BaseModel(DjangoCassandraModel):
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    created_at = columns.DateTime()
    updated_at = columns.DateTime()

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.datetime.utcnow()
        self.updated_at = datetime.datetime.utcnow()
        return super().save(*args, **kwargs)
    
    class Meta:
        abstract = True

class StellarAccountInquiryHistory(BaseModel):
    """
    A model for storing the history of user requests to examine a Stellar account.

    NOTE: To prevent multiple requests for the same Stellar account, ask the user
    if they want to make a new request or retrieve data from previous requests for
    that Stellar account.
    
    This model has three fields:
        - id: an AutoField for storing a unique identifier for each record
        - stellar_account_address: a Text for storing the address of the Stellar account
        - status: a Text for storing the status of the request
        - created_at: a DateTime for storing the date and time when the request was made
        - updated_at: a DateTime for storing the date and time when the request was last updated
    """

    stellar_account_address = columns.Text(max_length=56)
    network_name = columns.Text(max_length=9, default=TESTNET)
    status = columns.Text(max_length=20, default=PENDING)

class StellarAccountInquiryDetail(BaseModel):
    """
    A model for storing detailed information about user requests to examine a Stellar account.
    
    This model has six fields:
        - id: an AutoField for storing a unique identifier for each record
        - stellar_account_address: a Text for storing the address of the Stellar account
        - uri_endpoint: a Text for storing the URI endpoint of the request
        - response: a Text for storing the response to the request as a string
        - status: a Text for storing the status of the request
        - created_at: a DateTime for storing the date and time when the request was made
        - updated_at: a DateTime for storing the date and time when the request was last updated
    """

    stellar_account_address = columns.Text(max_length=56)
    network_name = columns.Text(max_length=9, default=TESTNET)
    uri_endpoint = columns.Text(max_length=200)
    response = columns.Text()
    status = columns.Text(max_length=20, default=PENDING)
