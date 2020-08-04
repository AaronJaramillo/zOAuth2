from bitcoinrpc.authproxy import AuthServiceProxy

node = AuthServiceProxy('http://user:password@0.0.0.0:38232')
node.generate(1)
print(node.z_gettotalbalance())
#print(node.z_listaddresses())
#print(node.getbalance())
#print(node.getnewaddress())
taddr = 'tmQj7xUdizNE8uNqiDBkVUBtNrydkQtjpn4'
#
print(node.sendtoaddress(taddr, 100))
print(node.generate(3))
#
#zaddy = 'zregtestsapling1xv2nxauz35zlh2klhr54plkssyxrantz6jp4843mtv55rmu74ppqcxlfk70dm3c3kah6uvhsycl'
#print(zaddy)
#node.z_sendmany('tmQj7xUdizNE8uNqiDBkVUBtNrydkQtjpn4', [
#    {
#        "address": zaddy,
#        "amount": 1,
#        "memo": "2d2d2d2d2d424547494e205055424c4943204b45592d2d2d2d2d0a4d466b77457759484b6f5a497a6a3043415159494b6f5a497a6a30444151634451674145766f452f6d2f6c3247477354312f4a7a4361626672776179505379480a626f7071385a30674b7a56305a644561455934683558316f6d2f6451583647596c634937682b48614e486e2b564a6c6f71664f6a5479562f4d773d3d0a2d2d2d2d2d454e44205055424c4943204b45592d2d2d2d2d0a"
#    },
#])
#node.generate(5)
##
##print(node.z_getbalance('zregtestsapling1lahh8cuqgfda3gtkqxhqc5k9j9em7l0l84ujtf4zmuv2tkf0zwufqwtymrrq488cdzc56wg67f7'))
##
##print(node.generate(3))
#
#print(node.z_listreceivedbyaddress(zaddy))
#print(node.z_listaddresses())
#print(node.z_listunspent())
print(node.listunspent(1, 999999999, [taddr]))
#print(node.z_getbalance(zaddy))
#ops = node.z_listoperationids()
#print(node.z_getoperationstatus(ops))
