a = [("a",0.1),("b",0.2),("c",0.15)]
print a
b = sorted(a,key=lambda a_tuple:a_tuple[1],reverse=1)
print b