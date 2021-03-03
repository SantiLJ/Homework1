# Santiago Le Jeune ; santiago.le.jeune@duke.edu; 02/25/2021

from os import listdir, remove

# If the io following files are in the current directory, remove them!
# 1. 'currency_pair.txt'
# 2. 'currency_pair_history.csv'
# 3. 'trade_order.p'

def check_for_and_del_io_files():
    dirs = set(listdir())
    if 'currency_pair.txt' in dirs:
        remove('currency_pair.txt')
    elif 'currency_pair_history.csv' in dirs:
        remove('currency_pair_history.csv')
    elif 'trade_order.p' in dirs:
        remove('trade_order.p')
    pass # nothing gets returned by this function, so end it with 'pass'.