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
        

3.namespace命名空间
  例子：
  	class A:
  		C = 10
		def __init__(self,name):
			self._name = name
		def print_name(self):
			print(self._name)
	class B(A):
		def __init__(self,name):
			super().__init__(name)
		def say_hello(self):
			print("hello"+self._name)
	a = A("jone")
	A:
	  C print_name
	B：
	  say_hello
	a:
	  _name
4.特性和描述符
	property
	__set__ __get__ __delete__
