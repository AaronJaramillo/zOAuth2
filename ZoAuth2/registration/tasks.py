from bitcoinrpc.authproxy import AuthServiceProxy
from socket import error as socket_error
from .models import Product, Transaction, Currency
from ZoAuth2 import settings

def query_transactions():
    """query_transactions."""
    node = AuthServiceProxy(settings.RPC_API_URL)
    currency = Currency.objects.select_for_update().get(ticker=settings.DEFAULT_CURRENCY)


    #get the block count from the node
    current_block = node.getblockcount()
    print(current_block)

    for product in Product.objects.all():
        #get all transactions with minimum confs for each adress in products
        ##TODO
        print('Scanning transactions from address: ' + product.address)
        transactions = node.z_listreceivedbyaddress(product.address, settings.REQUIRED_CONFS)
        print('Number of tx recieved from node: ' + str(len(transactions)))

        for tx in transactions:
            #process transaction if the tx blockheight is less than the last block
            if tx['blockheight']-settings.REQUIRED_CONFS < currency.last_block:
                print('transaction in block already scanned')
                continue
            tx['address'] = product.address
            process_tx(tx, product)

    #update the last block
    currency.update_last_block(current_block)
    currency.save()


def process_tx(tx, product):
    transaction, created = Transaction.objects.select_for_update().get_or_create(
        txid=['txid'],
        address=tx['address'],
        amount=int(tx['amount']*(10**8)),
        memo=tx['memo'])

    if created:
        print('tx created')
        transaction.save()

        if tx['confirmations'] >= settings.REQUIRED_CONFS:
            print('confirmed')
            return transaction.process_transaction()

        else:

            print(tx['confirmations'])
            print('not confirmed')
    else:
        print('tx already exists')
        if tx['confirmations'] >= settings.REQUIRED_CONFS:
            print('confirmations')
            return transaction.process_transaction()
        else:
            print('not confirmed')
