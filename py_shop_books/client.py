from intuitlib.client import AuthClient
from quickbooks import QuickBooks


def connect(client_id=None, client_secret=None, refresh_token=None, redirect_uri=None, company_id=None,
            environment='sandbox'):

    auth_client = AuthClient(
            client_id=client_id,
            client_secret=client_secret,
            environment=environment,
            redirect_uri=redirect_uri
        )


    client = QuickBooks(
        auth_client=auth_client,
        refresh_token=refresh_token,
        company_id=company_id
    )

    return client
