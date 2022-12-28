from django.db import models


class StellarAccountInquiryHistory(models.Model):
    """
    A model for storing the history of user requests to examine a Stellar account.

    NOTE: To prevent multiple requests for the same Stellar account, ask the user
    if they want to make a new request or retrieve data from previous requests for
    that Stellar account.
    
    This model has three fields:
        - id: an AutoField for storing a unique identifier for each record
        - stellar_account_address: a CharField for storing the address of the Stellar account
        - status: a CharField for storing the status of the request
        - created_at: a DateTimeField for storing the date and time when the request was made
        - updated_at: a DateTimeField for storing the date and time when the request was last updated
    """
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    ERROR = 'error'
    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
        (ERROR, 'Error'),
    )
    id = models.AutoField(primary_key=True)
    stellar_account_address = models.CharField(max_length=56)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class StellarAccountInquiryDetail(models.Model):
    """
    A model for storing detailed information about user requests to examine a Stellar account.
    
    This model has six fields:
        - id: an AutoField for storing a unique identifier for each record
        - inquiry: a ForeignKey field that references the id field in the StellarAccountInquiryHistory model
        - stellar_account_address: a CharField for storing the address of the Stellar account
        - uri_endpoint: a CharField for storing the URI endpoint of the request
        - response: a TextField for storing the response to the request as a string
        - status: a CharField for storing the status of the request
        - created_at: a DateTimeField for storing the date and time when the request was made
        - updated_at: a DateTimeField for storing the date and time when the request was last updated
    """
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
    )
    id = models.AutoField(primary_key=True)
    inquiry = models.ForeignKey(StellarAccountInquiryHistory, on_delete=models.CASCADE)
    stellar_account_address = models.CharField(max_length=56)
    uri_endpoint = models.CharField(max_length=200)
    response = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)