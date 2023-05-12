from config import *


zksync = ZkSyncBuilder.build(ZKSYNC_URL)
eth_web3 = Web3(Web3.HTTPProvider(ETH_URL))

def sleeping(from_sleep, to_sleep):

    x = random.randint(from_sleep, to_sleep)
    for i in tqdm(range(x), desc='sleep ', bar_format='{desc}: {n_fmt}/{total_fmt}'):
        time.sleep(1)

def deposit(privatekey):

    try:
        amount = round(random.uniform(MIN_AMOUNT, MAX_AMOUNT), 8)

        account: LocalAccount = Account.from_key(privatekey)
        eth_provider = EthereumProvider(zksync, eth_web3, account)
        wei_amount = Web3.to_wei(amount, "ether")
        eth_token = Token.create_eth()
        gas_price = eth_web3.eth.gas_price
        operator_tip = eth_provider.get_base_cost(gas_limit=eth_provider.RECOMMENDED_DEPOSIT_L2_GAS_LIMIT, gas_per_pubdata_byte=800,gas_price=gas_price)

        l1_tx_receipt = eth_provider.deposit(token=eth_token,
                                             amount=wei_amount,
                                             gas_per_pubdata_byte=800,
                                             operator_tip=operator_tip)
        
        tx_status = l1_tx_receipt['status']
        if tx_status == 1:
            logger.success(f" Deposit ETH to ZkSync Era| Amount: {amount}")
            list_send.append(f'{STR_DONE}zkSync Era deposit | {account.address}')
        else:
            logger.error(f"Deposit ETH to ZkSync Era| Tx status: {tx_status}")
            list_send.append(f'{STR_CANCEL}zkSync Era deposit | {account.address}')    

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
            # logger.info(f'Waitting gas value {GWEI}...')
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