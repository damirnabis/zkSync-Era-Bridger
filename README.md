Скрипт бриджит ETH из Mainnet в zkSync Era и обратно (https://portal.zksync.io/bridge)

# Настройка config.py и данных :
1. В файл `private_keys.txt` выписываем приватные ключи кошельков построчно.
2. В файле `config.py` меняем значения переменных под себя (подробнее в самом файле)

# Запуск :
1. Команда отправляет ETH из сети Mainnet в сеть zkSync Era.
```
python 01_deposit.py
``` 
2. Команда отправляет ETH из сети zkSync Era обратно в сеть Mainnet (Примечание: сейчас вывод занимает 24 часа)
```
python 02_withdrawal.py
```
