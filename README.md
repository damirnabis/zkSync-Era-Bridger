
### <sub>Settings before launch.</sub>
1. Open `config.py` file 
2. Put your RPC provider links ZKSYNC_URL and ETH_URL (u can skip this step)
3. Put your MIN_PRICE and MAX_PRICE. Script will randomly choose a price between these values ​​to send to the bridge
4. Enter the GWEI ammount at which you would like to perform the transaction
5. In the `private_keys.txt` file, insert private keys each on a new line
6. Run a command: 
```
pip install -r requirements.txt
```

### <sub>Run script with command:</sub>
``` 
python main.py
```