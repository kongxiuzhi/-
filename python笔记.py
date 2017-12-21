1.正则表达式
    模块 re
    常用方法：
        find,findall,search,match,compile,group(0)全部结果，group(1)部分结果
    通配符：
        .*？  + * ？ [^] ^$ r'' \ (.*?) (?P<标记>\d+) (?:\d+) 

    re.match(pattern,string,flags) #re.match 尝试从字符串的开始匹配一个模式
    mypatterns = re.compile(r"string")
    mypatterns.match(string)

2.类内置方法
    1.  def __getattr__(self,name):
            pass
        getattr(obj1，attr1)#如果对象obj1含有属性attr1则返回attr1的值，否则执行__getattr__方法
        



