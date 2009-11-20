#!/usr/bin/python

import time

# test #1: while loop counter controlled
i = 0
t0 = time.time()
while i < 1000:
  i = i + 1
t1 = time.time()
print 'test #1 elapsed time =',t1-t0,' cycle period =',(t1-t0) / 1000

# test #2: for loop range controlled

t0 = time.time()
for i in range(1000):
  pass
t1 = time.time()
print 'test #2 elapsed time =',t1-t0,' cycle period =',(t1-t0) / 1000

# test #3: dictionary access
d = {0:'zero',1:'uno',2:'due',3:'tre',4:'quattro',5:'cinque',6:'sei',7:'sette'}
t0 = time.time()
for i in range(1000):
  a = d[i % 8]
t1 = time.time()
print 'test #3 elapsed time =',t1-t0,' cycle period =',(t1-t0) / 1000

# test #4: variable access
var = 1
t0 = time.time()
for i in range(1000):
  a = var
t1 = time.time()
print 'test #4 elapsed time =',t1-t0,' cycle period =',(t1-t0) / 1000

# test #5: attribute access
class A:
  a = 1
a = A()
t0 = time.time()
for i in range(1000):
  b = a.a
t1 = time.time()
print 'test #5 elapsed time =',t1-t0,' cycle period =',(t1-t0) / 1000

# test #6: id access
a = 1
t0 = time.time()
for i in range(1000):
  b = id(a)
t1 = time.time()
print 'test #6 elapsed time =',t1-t0,' cycle period =',(t1-t0) / 1000

# test #7: dictionary access with long keys
a = {'01234567890123456789':'aaaabbbbccccdddd'}
t0 = time.time()
for i in range(1000):
  b = a['0123456789'+'0123456789']
t1 = time.time()
print 'test #7 elapsed time =',t1-t0,' cycle period =',(t1-t0) / 1000

# test #8: dictionary access with tuple key
class AA:
  pass
aa = AA()
ss = '0123456789'
a = {(aa,ss):'aaaabbbbccccdddd'}
t0 = time.time()
for i in range(1000):
  t = (aa,ss)
  b = a[t]
t1 = time.time()
print 'test #8 elapsed time =',t1-t0,' cycle period =',(t1-t0) / 1000

