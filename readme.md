#### mcQueue 为以 Python 和 memcache 为基础的 同步循环队列 ，可用于多线程和多进程读写同步。

#### mcLock 为基于 memcache 实现的 全局同步锁 ，用于读写同步。
<br/>
mcQueue 使用例子：

```python
import memcache
import mcQueue
mc = memcache.Client(["localhost:11211"])
mcqueue = mcQueue.mcQueue( mc , "your_project_name" )
mcqueue.push("test") # string
mcqueue.push(1) # integer
mcqueue.push(3.1415926535897932384626433832795028841971693993751) # float
mcqueue.push( [1, 2, 'hello'] ) # list
mcqueue.push( { 'key1':1, 'key2':'love you.' } ) # dict

elem = mcqueue.pop()
while elem != None:
    print elem
    elem = mcqueue.pop()

mcqueue.push( 'hello,ysunlin.' )
mcqueue.clear() # clear all the elements.
print mcqueue.pop()

mcqueue.push(1)
print mcqueue.popif(2)
print mcqueue.getTop() # just query the element, but pop it.
print mcqueue.popif(1)
print mcqueue.getTop() # just query the element, but pop it.
```

<br/>
mcLock使用例子：
```python
import memcache
import mcLock
mc = memcache.Client(["localhost:11211"])
mc = mcLock.mcLock( mc , "your_project_name" )
mc.lock()

mc.set('haha', "I'm Ysun Lin.")
mc.get('haha')
mc.add('shit', "I lost my love.")
mc.delete('haha')
mc.delete('shit')

mc.unlock()
```
