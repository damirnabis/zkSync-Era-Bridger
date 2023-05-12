from web3.middleware import geth_poa_middleware
from zksync2.transaction.transaction_builders import TxWithdraw
from config import *


web3 = ZkSyncBuilder.build(ZKSYNC_URL)
eth_web3 = Web3(Web3.HTTPProvider(ETH_URL))

def sleeping(from_sleep, to_sleep):

    x = random.randint(from_sleep, to_sleep)
    for i in tqdm(range(x), desc='sleep ', bar_format='{desc}: {n_fmt}/{total_fmt}'):
        time.sleep(1)

def withdrawal(privatekey):

    try:
        
        account: LocalAccount = Account.from_key(privatekey)
        
        # amount = web3.zksync.get_balance(account.address, EthBlockParams.LATEST.value)
        amount = round(random.uniform(MIN_AMOUNT, MAX_AMOUNT), 8)
  
        eth_web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        eth_balance = eth_web3.eth.get_balance(account.address)
        logger.info(f"Eth: balance: {Web3.from_wei(eth_balance, 'ether')}")

        eth_provider = EthereumProvider(web3,
                                        eth_web3,
                                        account)
        withdrawal = TxWithdraw(web3=web3,
                                token=Token.create_eth(),
                                amount=Web3.to_wei(amount, "ether"),
                                gas_limit=0,  # unknown
                                account=account)
        estimated_gas = web3.zksync.eth_estimate_gas(withdrawal.tx)
        tx = withdrawal.estimated_gas(estimated_gas)
        signed = account.sign_transaction(tx)
        tx_hash = web3.zksync.send_raw_transaction(signed.rawTransaction)
        logger.info(f"ZkSync Tx: https://goerli.explorer.zksync.io/tx/{web3.to_hex(tx_hash)}")
        list_send.append(f'{STR_DONE}zkSync Era withdrawal | {account.address}')
        # zks_receipt = web3.zksync.wait_finalized(tx_hash, timeout=3660, poll_latency=0.5)
        # logger.info(f"ZkSync Tx status: {zks_receipt['status']}")
        # tx_receipt = eth_provider.finalize_withdrawal(zks_receipt["transactionHash"])
        # logger.info(f"Finalize withdrawal, Tx status: {tx_receipt['status']}")

        # prev = eth_balance
        # eth_balance = eth_web3.eth.get_balance(account.address)
        # logger.info(f"Eth: balance: {Web3.from_wei(eth_balance, 'ether')}")

        # fee = tx_receipt['gasUsed'] * tx_receipt['effectiveGasPrice']
        # withdraw_absolute = Web3.to_wei(amount, 'ether') - fee
        # diff = eth_balance - prev
        # if withdraw_absolute == diff:
        #     logger.success(f"Withdrawal including tx fee is passed | Eth diff with fee included: {Web3.from_wei(diff, 'ether')}")
        #     list_send.append(f'{STR_DONE}zkSync Era withdrawal | {account.address}')
        # else:
        #     logger.error(f"Withdrawal failed | Eth diff with fee included: {Web3.from_wei(diff, 'ether')}")
        #     list_send.append(f'{STR_CANCEL}zkSync Era withdrawal | {account.address}')
    
    except Exception as error:
        logger.error(f'Withdrawal ETH from ZkSync Era| {error}')
        list_send.append(f'{STR_CANCEL}zkSync Era withdrawal | {account.address}')

if __name__ == "__main__":
    
    with open("private_keys.txt", "r") as f:
        keys_list = [row.strip() for row in f]
    
    random.shuffle(keys_list)

    for privatekey in keys_list:
        cprint(f'\n=============== start : {privatekey} ===============', 'yellow')
        withdrawal(privatekey)
        sleep = random.randint(SLEEP_TIME_MIN, SLEEP_TIME_MAX)
        sleeping(sleep,sleep)

    if TG_BOT_SEND == True:
        send_msg()     