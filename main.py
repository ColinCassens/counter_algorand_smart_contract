from helper import *
from counterAlgorandSmartContract import *
from algosdk import *

creator_mnemonic = "REPLACE WITH MNEMONIC"
algod_address = "http:localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

def main():
    # Init Client
    algod_client = algod.AlgodClient(algod_token=algod_token, algod_address=algod_address)

    # Get Private Keys
    creator_private_key = get_private_key_from_mnemonic(creator_mnemonic)

    # Declare application state storage (immutable)
    local_ints = 0
    local_bytes = 0
    global_ints = 1
    global_bytes = 0
    global_schema = transaction.StateSchema(global_ints, global_bytes)
    local_schema = transaction.StateSchema(local_ints, local_bytes)

    # Compile to TEAL Assembly
    print("---------------------------------------------")
    print("Compiling Teal...")

    with open("./approval.teal", "w") as f:
        approval_program_teal = approval_program()
        f.write(approval_program_teal)

    with open("./clear.teal", "w") as f:
        clear_state_program_teal = clear_state_program()
        f.write(clear_state_program_teal)

    # Compile to Binary
    print("Compiling Binary...")
    approval_program_compiled = compile_program(algod_client, approval_program_teal)
    clear_state_program_compiled = compile_program(algod_client, clear_state_program_teal)

    print("---------------------------------------------")
    print("Deploying Application...")

    # Create New Application
    app_id = create_app(algod_client, creator_private_key,
                        approval_program_compiled, clear_state_program_compiled,
                        global_schema, local_schema)

    # Read the global state
    print("Global State: ", read_global_state(algod_client,
                                              account.address_from_private_key(creator_private_key),
                                              app_id))

