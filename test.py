import json
import os

from web3 import Web3

from contract import compiled_sol


# ethereum_url = "https://ropsten.infura.io/v3/ff29ae16fe7b480a891578e366421e2e"
ethereum_url = "http://localhost:8545"
contract_address = '0x2f29dd992b68789f87b43b222d81445a4d134959'
acc_address = "0x59f879A2064EfF8238e8B63b654217C30f4e7c44"
priv_key = '67c1e4e00624e47934f486cdc7dc0330f5971edf1b2e4b1d864357fedffadd4a'

web3 = Web3(Web3.HTTPProvider(ethereum_url))
print('block number is', web3.eth.blockNumber)

balance = web3.eth.getBalance(acc_address)
print('balance is', balance)

account = web3.eth.account.privateKeyToAccount(priv_key)

bytecode = compiled_sol['contracts']['HashStorage.sol']['HashStorage']['evm']['bytecode']['object']
abi = json.loads(compiled_sol['contracts']['HashStorage.sol']['HashStorage']['metadata'])['output']['abi']

print('bytecode is', bytecode)
print('abi is', abi)

contract = web3.eth.contract(address=web3.toChecksumAddress(contract_address), abi=abi)

tx = contract.functions.registerHash(123456789)
print(tx)
tx.transact()
# print('tx_hash =', tx_hash)
# tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
# print(tx_receipt)

# c = web3.eth.contract(abi=abi, bytecode=bytecode)
#
# signed = web3.eth.account.sign_transaction(tx, priv_key)
# print('signed trans is', signed)
#
# trans_hash = web3.eth.sendRawTransaction(signed.rawTransaction)
# print('transaction hash is', trans_hash)

# print('waiting for transactionn confirmation...')
# tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
# print('confirmed!')

# contract_address = tx_receipt.contractAddress

# print('contract address is', contract_address)
