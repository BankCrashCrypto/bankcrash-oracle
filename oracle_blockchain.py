#%%
import config_test_acc
from web3 import Web3
import json

infura_url = config_test_acc.infura_url
w3 = Web3(Web3.HTTPProvider(infura_url))

contract_address = config_test_acc.contract_address
with open(config_test_acc.contract_abi_file, "r") as f:
  contract_abi = json.load(f)["abi"]

contract = w3.eth.contract(address=contract_address, abi=contract_abi)


def write_to_blockchain(is_small_bank_crash, is_middle_bank_crash, is_lage_bank_crash):
  nonce = w3.eth.get_transaction_count(config_test_acc.account_address)

  txn_dict = contract.functions.updateBankCrashEvents(is_lage_bank_crash, is_middle_bank_crash, is_small_bank_crash).build_transaction({
      'chainId':
      w3.eth.chain_id,
      'gas':
      700000,
      'gasPrice':
      w3.to_wei('1', 'gwei'),
      # 'maxFeePerGas': w3.to_wei('2', 'gwei'),
      # 'maxPriorityFeePerGas': w3.to_wei('1', 'gwei'),
      'nonce':
      nonce,
  })
  print(contract.functions.bankCrashEvents().call())
  print(txn_dict)
  signed_txn = w3.eth.account.sign_transaction(txn_dict, private_key=config_test_acc.account_private_key)
  # rr = w3.to_hex(w3.keccak(signed_txn.rawTransaction))

  result = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
  # print("progressing")
  print(result)
  tx_receipt = w3.eth.wait_for_transaction_receipt(result)
  print("DONE!")
  print(tx_receipt)


def read_blockchain():
  return contract.functions.bankCrashEvents().call()


def sync_blockchain_information(small_bank_crash, middle_bank_crash, lage_bank_crash):
  blockchain_crashes = read_blockchain()
  print("Current...", blockchain_crashes, "expected (", small_bank_crash, middle_bank_crash, lage_bank_crash, ")")
  while (blockchain_crashes[0] < small_bank_crash or blockchain_crashes[1] < middle_bank_crash or blockchain_crashes[2] < lage_bank_crash):
    # write_to_blockchain(blockchain_crashes[0] < small_bank_crash, blockchain_crashes[1] < middle_bank_crash, blockchain_crashes[2]
    #                     < lage_bank_crash)
    blockchain_crashes[0] += blockchain_crashes[0] < small_bank_crash
    blockchain_crashes[1] += blockchain_crashes[1] < middle_bank_crash
    blockchain_crashes[2] += blockchain_crashes[2] < lage_bank_crash
    print("Syncing...", blockchain_crashes)

  return


# write_to_blockchain(False, False, True)
# sync_blockchain_information(5, 3, 2)
# %%
