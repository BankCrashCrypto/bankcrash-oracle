#%%
import config_test_acc
from web3 import Web3

infura_url = config_test_acc.infura_url
w3 = Web3(Web3.HTTPProvider(infura_url))

#%%
import json

contract_address = config_test_acc.contract_address
with open(config_test_acc.contract_abi_file, "r") as f:
	contract_abi = json.load(f)

# Create contract instance
contract = w3.eth.contract(address=contract_address, abi=contract_abi)


def write_to_blockchain(is_small_bank_crash, is_middle_bank_crash, is_lage_bank_crash):
    # replace 'YOUR_ACCOUNT_ADDRESS' and 'YOUR_PRIVATE_KEY' with your Ethereum account address and private key
    nonce = w3.eth.getTransactionCount(config_test_acc.account_address)

		# function_to_call=updateBankCrashEvents(bool bigBankCrashEvent, bool mediumBankCrashEvent, bool smallBankCrashEvent)

    txn_dict = contract.functions.updateBankCrashEvents(is_lage_bank_crash, is_middle_bank_crash, is_small_bank_crash).buildTransaction({
        'chainId': 1,
        'gas': 70000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'nonce': nonce,
    })

    signed_txn = w3.eth.account.signTransaction(txn_dict, private_key=config_test_acc.account_private_key)

    result = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

    tx_receipt = w3.eth.waitForTransactionReceipt(result)

    print(tx_receipt)

# %%
# %%
