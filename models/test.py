# coding=gbk
string = '我的'
print "string is:", type(string)
print string

ustring = u"我的"
print "ustring is:", type(ustring)
print ustring

gbkstring = ustring.encode("gbk")
print "gbkstring is:", type(gbkstring)
print gbkstring

anotherstring = gbkstring.decode("gbk")
print "anotherstring is:", type(anotherstring)
print anotherstring
