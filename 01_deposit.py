from config import *


zk_web3 = ZkSyncBuilder.build(ZKSYNC_URL)
eth_web3 = Web3(Web3.HTTPProvider(ETH_URL))

def deposit(privatekey):
    
    try:
        amount = round(random.uniform(MIN_AMOUNT, MAX_AMOUNT), 8)

        account: LocalAccount = Account.from_key(privatekey)

        eth_provider = EthereumProvider(zk_web3, eth_web3, account)

        gas_price = eth_web3.eth.gas_price
        gas_limit = 710000

        print(f"Executing deposit transaction on L1 network, amount {amount}")
        operator_tip = eth_provider.get_base_cost(gas_limit=gas_limit, gas_per_pubdata_byte=800,gas_price=gas_price)

        l1_tx_receipt = eth_provider.deposit(token=Token.create_eth(),
                                             amount=Web3.to_wei(amount, 'ether'),
                                             l2_gas_limit=gas_limit,
                                             gas_price=gas_price,
                                             gas_per_pubdata_byte=800,
                                             operator_tip=operator_tip)

        if not l1_tx_receipt["status"]:
            logger.error(f"https://etherscan.io/tx//{l1_tx_receipt['transactionHash'].hex()}")
            list_send.append(f'{STR_CANCEL}zkSync Era deposit | {account.address}')
            return
    
        logger.success(f"https://etherscan.io/tx//tx/{l1_tx_receipt['transactionHash'].hex()}")
        list_send.append(f'{STR_DONE}zkSync Era deposit | {account.address}')
   
        # zksync_contract = ZkSyncContract(zk_web3.zksync.main_contract_address, eth_web3, account)

        # l2_hash = zk_web3.zksync.get_l2_hash_from_priority_op(l1_tx_receipt, zksync_contract)

        # print("Waiting for deposit transaction on L2 network to be finalized (5-7 minutes)")
        # l2_tx_receipt = zk_web3.zksync.wait_for_transaction_receipt(transaction_hash=l2_hash,
        #                                                                     timeout=360,
        #                                                                     poll_latency=10)

        # return l1_tx_receipt['transactionHash'].hex() , l2_tx_receipt['transactionHash'].hex()
    
    except Exception as error:
        logger.error(f'Deposit ETH to ZkSync Era| {error}')
        list_send.append(f'{STR_CANCEL}zkSync Era deposit | {account.address}')
    
if __name__ == "__main__":
    
    with open("private_keys.txt", "r") as f:
        keys_list = [row.strip() for row in f]
    
    random.shuffle(keys_list)

    for privatekey in keys_list:
        cprint(f'\n=============== start : {privatekey} ===============', 'yellow')
        
        if GWEI == "":
            deposit(privatekey)
        else:     
            stop_this_shit = False
            while not stop_this_shit:
                gas_price = eth_web3.eth.gas_price
                gwei_gas_price = eth_web3.from_wei(gas_price, 'gwei')

                if gwei_gas_price <= GWEI:    
                    deposit(privatekey)
                    stop_this_shit = True
                else:
                    logger.info(f'Waitting gas value {GWEI}(current gas {gwei_gas_price})')
                    sleeping(30,30)    
        
        sleep = random.randint(SLEEP_TIME_MIN, SLEEP_TIME_MAX)
        sleeping(sleep,sleep)

    if TG_BOT_SEND == True:
        send_msg()     