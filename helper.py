import base64

from algosdk import *

'''
https://developer.algorand.org/docs/get-details/dapps/pyteal/
'''

def compile_program(client, source_code):
    compile_response = client.compile(source_code)
    return base64.b64decode(compile_response['result'])

def get_private_key_from_mnemonic(mn):
    private_key = mnemonic.to_private_key(mn)
    return private_key

def wait_for_confirmation(client, transaction_id, timeout):
    start_round = client.status()['last-round'] + 1
    current_round = start_round

    while current_round < start_round + timeout:
        try:
            pending_txn = client.pending_transaction_info(transaction_id)
        except Exception:
            return
        if pending_txn.get("confirmed-round", 0) > 0:
            return pending_txn
        elif pending_txn['pool-error']:
            raise Exception('pool-error: {}'.format(pending_txn['pool-error']))

        client.status_after_block(current_round)
        current_round += 1
    raise Exception(
        'pending txn not found in timeout rounds, timeout value = : {}'.format(timeout)
    )

'''
Formats application data for display
'''
def format_state(state):
    formatted = {}
    for item in state:
        key = item['key']
        value = item['value']
        formatted_key = base64.b64decode(key).decode('utf-8')
        if value['type'] == 1:
            # byte string type
            if formatted_key == 'voted':
                formatted_value = base64.b64decode(value['bytes']).decode('utf-8')
            else:
                formatted_value = value['bytes']
            formatted[formatted_key] = formatted_value
        else:
            # integer type
            formatted[formatted_key] = value['uint']
    return formatted

'''
Read the application global state
- connects to the node and retrieves the information from the owners ledger entry on the blockchain
- the owners ledger entry in the blockchain holds the app data for all of their created applications
'''
def read_global_state(client, addr, app_id):
    results = client.account_info(addr)
    apps_created = results['created-apps']
    for app in apps_created:
        if app['id'] == app_id:
            return format_state(app['params']['global-state'])
    return {}

'''
Create New Application
'''
def create_app(client, private_key, approval_program, clear_program, global_schema, local_schema):

    # Define sender as creator
    sender = account.address_from_private_key(private_key)

    # Declare on_complete as NoOp
    on_complete = transaction.OnComplete.NoOpOC.real

    # Get node suggested parameters
    params = client.suggested_params()

    # Create Unsigned Transaction
    txn = transaction.ApplicationCreateTxn(sender, params, on_complete, approval_program, clear_program, global_schema, local_schema)

    # Sign Txn
    signed_txn = txn.sign(private_key)
    txn_id = signed_txn.transaction.get_txid()

    # Send Txn
    client.send_transactions([signed_txn])

    # Wait for confirmation
    wait_for_confirmation(client, txn_id, 5)

    # Display results
    transaction_response = client.pending_transaction_info(txn_id)
    app_id = transaction_response['application-index']
    print("Created new app-id", app_id)

    return app_id


