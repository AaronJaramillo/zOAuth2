from bitcoinrpc.authproxy import AuthServiceProxy

node = AuthServiceProxy('http://user:password@0.0.0.0:38232')

address = node.getnewaddress()#'tmQj7xUdizNE8uNqiDBkVUBtNrydkQtjpn4'

#node.generate(500)
print(node.sendtoaddress(address, 100))
node.generate(10)
print(address)
