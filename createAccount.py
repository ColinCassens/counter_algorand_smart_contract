from algosdk import account, mnemonic
from algosdk.v2client import algod

def get_sandbox_client():
    address = "http://localhost:4001"
    token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    return algod.AlgodClient(token, address)

def create_new_wallet():
    private_key, address = account.generate_account()
    f = open("accounts", "a")
    f.write('\n\n-----------------------------------\n')
    f.write('\nAddress: {}'.format(address))
    f.write('\nPrivate Key: {}'.format(private_key))
    f.write('\nMnemonic: {}'.format(mnemonic.from_private_key(private_key)))
    f.close()
    print('Address: {}'.format(address))
    print('Private Key: {}'.format(private_key))
    print('Mnemonic: {}'.format(mnemonic.from_private_key(private_key)))

'''
To Add funds to test wallet
https://dispenser.testnet.aws.algodev.network/
'''
def check_balance(address):
    client = get_sandbox_client()
    account_info = client.account_info(address)
    print("Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")

def update_backup():
    accounts = open("accounts", "r")
    backup = open("accounts_backup", "w")
    for line in accounts.readlines():
        backup.write(line)
    accounts.close()
    backup.close()

if __name__ == "__main__":
    # create_new_wallet()
    address1 = ""
    # address2 = ""
    #
    check_balance(address1)
    # update_backup()
