
'''

django BLOG 总结

'''
环境配置
        sudo apt-get install
	zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel
	
	tk-devel python-devel python3-devel gcc make pip apache2 libapache2-mod-wsgi-py3 mysql-server mysql-client libmysqlclient-dev
	postgresql
	pip install
	virtualenv django pillow pytz psycopg2
正确的配置apache && django && mod_wsgi
    1.python源码安装 ./configure --enable-shared #和mod_wsgi有关
    2.apache 安装
    3.mod_wsgi源码安装 --with-pyhon=/usr/local/bin/python3 #指定python版本
    4.vim /etc/selinux/config
        修改SELINUX=disabled
        重起后生效！
        重起后生效！
    5.配置apache
       1.在httpd.conf添加LoadModule wsgi_module modules/mod_wsgi.so 
        #否则无法加载wsgi报错，mod_wsgi.so 被mod_wsgi安装在modules中了
       2.编写wsgi配置文件
            创建django.conf文件添加如下代码
            
            #自己网站要监听的端口，根据IP 端口 ServerName|ServerNameAlias 确定网站app
            Listen 8080
            #监听本主机所有ip地址的8080端口
            <VirtualHost *:8080>
            #IP:端口相同 服务器名不同，这个虚拟机监听 *：8080:www.blog.com
            ServerName www.blog.com
            #指定守护进程的名字和虚拟环境下使用python的路径和工程目录
            WSGIDaemonProcess  blog python-path=/home/myven/dgp:/home/myven/lib/python3.6/site-packages
            #指定进程组名
            WSGIProcessGroup blog
            #指定django真实的wsgi的位置
            WSGIScriptAlias / /home/myven/dgp/blog/blog/wsgi.py
            Alias /static/ /home/myven/dgp/blog/static/
            Alias /media/ /home/myven/dgp/blog/media/
            <Directory /home/myven/dgp/blog/static>
            Require all granted
            </Directory>
            <Directory /home/myven/dgp/blog/media>
            Require all granted
            </Directory>
            <Directory /home/myven/dgp/blog/blog>
            <Files wsgi.py>
            Require all granted
            </Files>
            </Directory>
            </VirtualHost>
    6.配置django
        1.settings.py
            ALLOWED_HOSTS = ["*"]#所有地址

            STATIC_URL = '/static/'
            STATIC_ROOT = os.path.join(BASE_DIR,"static/")
            #运行 python manage.py collectstatic 收集adminset的静态文件

            MEDIA_URL = '/media/'
            MEDIA_ROOT = os.path.join(BASE_DIR,"media/")
        2.wsgi.py
            添加
            import sys
            form os.path import join,dirname,abspath
            PROJECT_DIR = dirname(dirname(abspath(__file__)))
            sys.path.insert(0,PROJECT_DIR)#否则会报错
    7.centos7 apache 权限管理
        chmod -R 755 myproject
        chmod -R 775 media/uploads#上全文件的文件夹

1.python 安装
    ./configure --enable-shared --prefix=/usr/local/python3

    error:
        python3.6: error while loading shared libraries: 
        libpython3.6m.so.1.0: cannot open shared object file:
        No such file or directory
    solution:
        #echo "/usr/local/python3/lib" > /etc/ld.so.conf.d/python3.6.conf
        #ldconfig
        或者没有指定prefix目录 
        #echo "/usr/local/lib" > /etc/ld.so.conf.d/python3.6.conf
        #ldconfig
2.安装mod_wsgi
    error
        mod_wsgi的版本对应不同的python版本
    solution
        1.下载mod_wsgi源码包
        2.tar -zxvf mod_wsgi.x.x.tar.gz
        3.编译安装 
            ./configure --help
            ./configure --with-python=/usr/local/bin/python3 #要使用的python版本
            make && make install
        注：mod_wsgi.so 自动安装到httpd/moduls中了
            配置apache时使用

        在虚拟环境中安装mod_wsgi
        1.安装python3
            ./configure --enable-shared
        2.按装virtualenv
            pip3 install virtualenv
        3.创建虚拟环境
            virtualenv -p [python2|python3] myvenname
        4.激活虚拟环境
            source myvenname/bin/activate 
            推出
                deactivate
        5.安装mod_wsgi
            pip install mod_wsgi
        原因
            mod_wsgi.so  ?
3.安装配置apache && 配置mod_wsgi
    安装apache
    systemctl start httpd
    systemctl enable httpd

    主配置文件/etc/httpd/conf/httpd.conf
    加载的个人配置文件目录/etc/httpd/conf.d/myhttpd.conf

    error
        在使用虚拟环境的工程中，设置wsgi配置中别名和文件权限时路径不完整，没有
        把虚拟环境的文件路径包含进去 
        例如：
            WSGIDaemonProcess  blog python-path=/home/myven/dgp:/home/myven/lib/python3.6/site-packages
            /home/:主目录
            myven/:虚拟环境目录
            dgp/:虚拟环境下自定义的文件夹，里面包含着工程文件

  



sys.path.insert()
755 root:root
775 上传文件权限 
    myproject/media/uploads
    chmod -R 775 uploads

1.setting配置

	DEBUG = True|False

	ALLOWED_HOST = ['*']

	app注册：
	     INSTALL_APPS =[
	     	'myapp.apps.MappConfig',

	     ]

	templates位置：
		1：各个APP的根目录 myapp/templates
		2：project 的根目录 Myproject/templates
			配置settings:
				TEMPLATES = [
					{
						'DIRS':[os.path.join(BASW_DIR,'templates')]
					}
				]
		3.全局template:
			TEMPLATES = [
						{
							'DIRS':[os.path.join(BASW_DIR,'templates')]
							'OPTIONS':{

									'myapp.views.global_setting'
							}
						}
					]
			在myapp/views.py下创建：
				from django.conf import settings
				def global_setting(request):
					return locals()
	数据库配置：
		工具：Navicat
		postgresql:
			sudo apt-get install postgresql
			pip install psycopg2
			更改postgres用户密码：
				sudo -u postgres psql
				ALTER USER postgres WITH PASSWORD '123456';
			postgres登陆：
				psql -h 127.0.0.1 -U postgres
			修改ubuntu root登陆postgres密码：
				su root
				sudo passwd -d postgres//删除密码
				sudo -u postgres passwd //设置密码
			重启服务：
				/etc/init.d/postgresql restart//默认端口：5432
			创建用户：
				create user "username" with password "passwords";
				create database "testdb" with owner = "username";
			settings配置：
				DATABASES = {
					'default':{
						'ENGINE':'django.db.backends.postgresql',
						'NAME':'database_name',
						'USER':'database_user_name',
						'PASSWORD':'database_user_password',
						'HOST':'database_service_ip',
						'PORT':'database_port',//'5432'
					}
				}
		msql:
			sudo apt-get install mysql-server
			sudo apt-get install mysql-client
			sudo apt-get install mysql-div
			驱动程序：
				MySQLdb,mysqlclient,mysqlclient(mysql官方推荐)，PyMySQL(纯python)
				pip install PyMySQL
				关键是这里：我们还需要在myproject的__init__.py文件中添加如下的内容：
				import pymusql
				pymysql.install_as_MySQLdb()

			msql.w002 error
			DATABASES = {
					'OPTIONS':{'init_commend':"SET sql_mode='STRICT_TRANS_TABLES'",
					'charset':'utf8md4',}
			}

	时区设置：
		pip install pytz
		settings配置：
			TIME_ZONE = 'Asia/Shanghai'
			USE_TZ = False

	静态文件配置：
		STATIC_RUL = '/static/'
		STATICFILES_DITS = (os.path.join(BASE_DIR,'static'),)// python manage.py collectstatic
		STATIC_ROOT = '/static/'

	配置上传文件件：
		MEDIA_URL = '/media/'
		MEDIA_ROOT = os.path.join(BASE_DIR,'media')
		权限设置：
			例如：/media/uploads为上传文件夹
			则：cd /media
			sudo chgrp -R www-data uploads
			sudo chmod -R g+w uploads
			一般目录权限设置为 755，文件权限设置为 644 
			假如项目位置在 /home/tu/zqxt （在zqxt 下面有一个 manage.py，zqxt 是项目名称）
			cd /home/tu/
			sudo chmod -R 644 zqxt
			sudo find zqxt -type d -exec chmod 755 \{\} \;
2.User扩展：
	在settings.py下添加：AUTH_USER_MODEL = 'Myapp.User'
	在Myapp.models下：
		from django.contrib.auth.models import AbstractUser
		class User(AbstractUser):
			mobile = models.CharField(max_length=11, blank=True, null=True, unique=True, verbose_name='手机号码')
			class Meta:
        		verbose_name = '用户'
        		verbose_name_plural = verbose_name
        	def __unicode__(self):
        		return self.username
    在Myapp.admin下：
		from django.contrib import admin
		from web_sso import models
		from django.contrib.auth.admin import UserAdmin  # 从django继承过来后进行定制
		from django.utils.translation import ugettext_lazy as _
		from django.contrib.auth.forms import UserCreationForm, UserChangeForm # admin中涉及到的两个表单




		# custom user admin
		class MyUserCreationForm(UserCreationForm):  # 增加用户表单重新定义，继承自UserCreationForm
		    def __init__(self, *args, **kwargs):
		        super(MyUserCreationForm, self).__init__(*args, **kwargs)
		        self.fields['email'].required = True   # 为了让此字段在admin中为必选项，自定义一个form
		        self.fields['mobile'].required = True  # 其实这个name字段可以不用设定required，因为在models中的MyUser类中已经设定了blank=False，但email字段在系统自带User的models中已经设定为
		        # email = models.EmailField(_('email address'), blank=True)，除非直接改源码的django（不建议这么做），不然还是自定义一个表单做一下继承吧。


		class MyUserChangeForm(UserChangeForm):  # 编辑用户表单重新定义，继承自UserChangeForm
		    def __init__(self, *args, **kwargs):
		        super(MyUserChangeForm, self).__init__(*args, **kwargs)
		        self.fields['email'].required = True
		        self.fields['mobile'].required = True


		class CustomUserAdmin(UserAdmin):
		    def __init__(self, *args, **kwargs):
		        super(CustomUserAdmin, self).__init__(*args, **kwargs)
		        self.list_display = ('username', 'mobile', 'email', 'is_active', 'is_staff', 'is_superuser')
		        self.search_fields = ('username', 'email', 'mobile')
		        self.form = MyUserChangeForm  #  编辑用户表单，使用自定义的表单
		        self.add_form = MyUserCreationForm  # 添加用户表单，使用自定义的表单
		        # 以上的属性都可以在django源码的UserAdmin类中找到，我们做以覆盖

		    def changelist_view(self, request, extra_context=None):  # 这个方法在源码的admin/options.py文件的ModelAdmin这个类中定义，我们要重新定义它，以达到不同权限的用户，返回的表单内容不同
		        if not request.user.is_superuser:  # 非super用户不能设定编辑是否为super用户
		            self.fieldsets = ((None, {'fields': ('username', 'password',)}),
		                              (_('Personal info'), {'fields': ('mobile', 'email')}),  # _ 将('')里的内容国际化,这样可以让admin里的文字自动随着LANGUAGE_CODE切换中英文
		                              (_('Permissions'), {'fields': ('is_active', 'is_staff', 'groups')}),
		                              (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
		                              )  # 这里('Permissions')中没有'is_superuser',此字段定义UserChangeForm表单中的具体显示内容，并可以分类显示
		            self.add_fieldsets = ((None, {'classes': ('wide',),
		                                          'fields': ('username', 'mobile', 'password1', 'password2', 'email', 'is_active',
		                                                     'is_staff', 'groups'),
		                                          }),
		                                  )  #此字段定义UserCreationForm表单中的具体显示内容
		        else:  # super账户可以做任何事
		            self.fieldsets = ((None, {'fields': ('username', 'password',)}),
		                              (_('Personal info'), {'fields': ('mobile', 'email')}),
		                              (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
		                              (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
		                              )
		            self.add_fieldsets = ((None, {'classes': ('wide',),
		                                          'fields': ('username', 'mobile', 'password1', 'password2', 'email', 'is_active',
		                                                     'is_staff', 'is_superuser', 'groups'),
		                                          }),
		                                  )
		        return super(CustomUserAdmin, self).changelist_view(request, extra_context)


		admin.site.register(models.MyUser, CustomUserAdmin)  # 注册一下
3.models
	1.创建绝对路由


		from django.urls import reverse
			def get_absolute_url(self):
				return reverse('app_name:urlname',args=[str(self.id)])
	2.创建admin中的别名：
		class Meta:
			verbose_name = "name"
			verbose_name_plural = verbose_name
	3.字段Choices：
		choices=,((),(),()),default=
	4.null,blank
		null数据库可以为空，blank表单可以为空
	5.ImageField
		1.在你的settings文件中, 你必须要定义 MEDIA_ROOT 作为Django存储上传文件的路径(从性能上考虑，这些文件不能存在数据库中。) 
		  定义一个 MEDIA_URL 作为基础的URL或者目录。确保这个目录可以被web server使用的账户写入。
		2.在模型中添加FileField 或 ImageField 字段, 定义 upload_to参数，内容是 MEDIA_ROOT 的子目录，用来存放上传的文件。
		3.数据库中存放的仅是这个文件的路径 （相对于MEDIA_ROOT). 你很可能会想用由Django提供的便利的url 属性。
		  比如说, 如果你的ImageField 命名为 mug_shot, 你可以在template中用 {{ object.mug_shot.url }}获得你照片的绝对路径。
		例如，如果你的 MEDIA_ROOT设定为 '/home/media'，并且 upload_to设定为 'photos/%Y/%m/%d'。
		 upload_to的'%Y/%m/%d'被strftime()所格式化；'%Y' 将会被格式化为一个四位数的年份, '%m' 被格式化为一个两位数的月份'%d'是两位数日份。
		 如果你在Jan.15.2007上传了一个文件，它将被保存在/home/media/photos/2007/01/15目录下.
	6.创建数据记录：
		1. Article.objects.create(title="title")
		2. at=Article(title="title")
			at.save()
		3.at = Article.objects.get(title="tilte")
		  at= Article.objects.get(pk=1)
		  at= Article.objects.filter(title="tilte")
		  at = Article.objects.value("title")
		  form django.db.models import Count
		  at.Count
		  at = Article.objects.annotate(num_book=Count('book'))
		  at.num_book
	7.创建model
		myModel.objects.create(field1=data1,field2=data2)
		myModel.save()
	8.filter,exclude,order_by,delect,values_list()
		Post.objects.filter(publish__year=2015,author__username='admin').exclude(title__startswith='Why')
		order_by("-publish")
		post = Post.object.get(id=1)
		post.delete()

		values_list()
		>>> Entry.objects.values_list('id').order_by('id')
		<QuerySet[(1,), (2,), (3,), ...]>
		>>> Entry.objects.values_list('id', flat=True).order_by('id')
		<QuerySet [1, 2, 3, ...]>
	9.创建Manager
		class PublishedManager(models.Manager):
			def get_queryset(self):
				return super(PublishedManager,self).get_queryset().filter(status='published')
		class Post(models.Model):
			objects = models.Manger()
			published = PublishedManager()
	10.#add a save() method 
		from django.utils.text import slugify
		class Image(models.Model):
		# ...
			def save(self, *args, **kwargs):
				if not self.slug:
					self.slug = slugify(self.title)
				super(Image, self).save(*args, **kwargs)
	11.manytomany self
		from django.contrib.auth.models import User
		class Contact(models.Model):
			user_from = models.ForeignKey(User,related_name='rel_from_set')
			user_to = models.ForeignKey(User,related_name='rel_to_set')
			created = models.DateTimeField(auto_now_add=True,db_index=True)
			class Meta:
				ordering = ('-created',)
			def __str__(self):
				return '{} follows {}'.format(self.user_from,self.user_to)
		#
		following = models.ManyToManyField('self',through=Contact,related_name='followers',symmetrical=False)
		User.add_to_class('following',models.ManyToManyField('self',through=Contact,
				related_name='followers',symmetrical=False))

4.admin
	自定义ACTIONS:
		def make_active(self,request,queryset):
			queryset.update(modelsfie = "推荐")
		make_recommend.short_description = "推荐文章"
		class MyMoelsAdmin(admin.ModelAdmin):
			actions =[make_active,]
	list_display =()#显示的子段
	search_fields = ()#查询的子段，对于外键需要制定父表的子段foreinkeymodel.__name
	prepopulated_fields={'slug':('title',)}#自动填充
	raw_id_fields = ('author',)
	date_hierarchy='publish'#按时间分段
	
	
	fields =()
	fieldsets ={
				("title",{'fields':('','')}),
				(None,{"fields":('','')}),
				(None,{'class':('wide',),"fields":('','')}),
		}
				

  	admin.site.register(mymodel,MyMoelsAdmin)
	@admin.register(MyModel)
5.form
	class MyForm(forms.Form):
		email = forms.EmailField(widget=forms.TextInput(max_length=50,error_messages={'required':"message"},
								attrs={
											'id':"email",'class':"email",
											'type':'email','size':'25',
											'required':'required','tabindex':'1',
										}))

	class MyForm(forms.ModelForm):
		class Meta:
			model = mymodel
			fields = ('name','password','content')
			widgets = {
				'name':forms.TextInput(max_length=50,error_messages={'required':'message'},
								attrs={'':}
								)
				'content':forms.Textarea(attrs={'cols':'50','rows':'5','placeholder':'请输入内容'})
			}		

	<form action="" method="post">
		{{csref_token}}
		{{myform.as_p}}
		<input type="submit" value="Submit"/>
	</form>	
	#clean_<fieldname>()
	def clean_url(self):
		url = self.cleaned_data['url']
		valid_extensions = ['jpg', 'jpeg']
		extension = url.rsplit('.', 1)[1].lower()
		if extension not in valid_extensions:
			raise forms.ValidationError('The given URL does not ' \
							'match valid image extensions.')
		return url

6.templates
	{%load staticfiles %}
	{% extends 'base.html'%}
	{%include 'ot.html'%}
	{% block content%}{%endblock%}
	{%for in %}{%endfor%}
	{%with as%}{%endwith%}
	{%if is not %}{%elif %}{%else%}{%endif%}
	{{content|safe|linebreaks|truncatechars|date:'Y-m-d'}}

	deal with 404 500 403 error
	1.in urls.py define handler
		handler404 = 'myapp.views.my_custom_pap_404_view'
	2.in templates create 404.html 500.html


	分页
		from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
		def post_list(request):
			object_list= Post.published.all()
			paginator = Paginator(object_list,3)#3 post in each page
			page = request.GET.get('page')
			try:
				posts = paginator.page(page)
			except PageNotAnInteger:
				posts = paginator.page(1)
			except EmptyPage:
				posts = paginator.page(paginator.num_pages)
			return render(request,'blog/post/list.html',{'page':page,'posts':posts})
		pagination.html
			<div class="pagination">
			<span class="step-links">
			{% if page.has_previous %}
			<a href="?page={{ page.previous_page_number }}">Previous</a>
			{% endif %}
			<span class="current">
			Page {{ page.number }} of {{ page.paginator.num_pages }}.
			</span>
			{% if page.has_next %}
			<a href="?page={{ page.next_page_number }}">Next</a>
			{% endif %}
			</span>
			</div>
		在需要使用到分页的html文档中
			{% block content %}
			...
			{% include "pagination.html" with page=posts %}
			{% endblock %}


7.login logout
	from django.contrib.auth import logout,login,authenticate
	from django.contrib.auth.hashers import make_password

	def logoutview(request):
		logout(request)
		return render()
	def loginview(request):
		user = authenticate(username,password)
		if user:
			user.backend = 'django.contrib.auth.backends.ModelBackend'
			login(request,user)
	if request.user.is_authenticated()://判断是否登陆
	获得登陆的用户名：name = request.user.username
8.富文本编辑器kindedtor
	1.在admin.py要使用富文本编辑器的（modeladmin）中添加：
		class Media:
		  	js = (
		  			'kindeditor-all.js',
		  			'lang/zh_CN.js',
		  			'myconfig.js'
			  		)
	2.myconfig.js
			kindeditor.ready(function(K){
				K.create('textarea[name=content]',
					{width:'800px',
					 height:'200px',
					 uploadJson:'/admin/media/kindeditor',
					});
				})
	3.url.py
		    url(r"^uploads/(?P<path>.*)$","django.views.static.serve",{"document_root": settings.MEDIA_ROOT,}),
    		url(r'^admin/upload/(?P<dir_name>[^/]+)$', upload_image, name='upload_image'),
    4.upload.py
    		# -*- coding: utf-8 -*-
			from django.http import HttpResponse
			from django.conf import settings
			from django.views.decorators.csrf import csrf_exempt
			import os
			import uuid
			import json
			import datetime as dt

			@csrf_exempt
			def upload_image(request, dir_name):
			    ##################
			    #  kindeditor图片上传返回数据格式说明：
			    # {"error": 1, "message": "出错信息"}
			    # {"error": 0, "url": "图片地址"}
			    ##################
			    result = {"error": 1, "message": "上传出错"}
			    files = request.FILES.get("imgFile", None)
			    if files:
			        result =image_upload(files, dir_name)
			    return HttpResponse(json.dumps(result), content_type="application/json")

			#目录创建
			def upload_generation_dir(dir_name):
			    today = dt.datetime.today()
			    dir_name = dir_name + '/%d/%d/' %(today.year,today.month)
			    if not os.path.exists(settings.MEDIA_ROOT + dir_name):
			        os.makedirs(settings.MEDIA_ROOT + dir_name)
			    return dir_name

			# 图片上传
			def image_upload(files, dir_name):
			    #允许上传文件类型
			    allow_suffix =['jpg', 'png', 'jpeg', 'gif', 'bmp']
			    file_suffix = files.name.split(".")[-1]
			    if file_suffix not in allow_suffix:
			        return {"error": 1, "message": "图片格式不正确"}
			    relative_path_file = upload_generation_dir(dir_name)
			    path=os.path.join(settings.MEDIA_ROOT, relative_path_file)
			    if not os.path.exists(path): #如果目录不存在创建目录
			        os.makedirs(path)
			    file_name=str(uuid.uuid1())+"."+file_suffix
			    path_file=os.path.join(path, file_name)
			    file_url = settings.MEDIA_URL + relative_path_file + file_name
			    open(path_file, 'wb').write(files.file.read()) # 保存图片
			    return {"error": 0, "url": file_url}

9.apache2 配置
    1. apache2.conf配置
        添加 ServerName 127.0.0.1
    2. 在sites-available中创建网站配置文件
        mysite.conf
	<VirtualHost *:80>

	    ServerName www.blog.com
	    ServerAlias localhost
	    ServerAdmin xiuzhikong@163.com
	    
	#    Alias /media/ /home/py3env/ERP/dms/media/
	#    Alias /static/ /home/py3env/ERP/dms/static/
	#    Alias /templates/ /home/py3env/ERP/dms/templates/
	    Alias /templates/ /home/py3env/Blog/templates/
	    Alias /static/ /home/py3env/Blog/static/
	    Alias /media/ /home/py3env/Blog/media/

	    <Directory /home/py3env/Blog/static>
	      Require all granted
	    </Directory>

	    <Directory /home/py3env/Blog/templates>
	      Require all granted
	    </Directory>

	    <Directory /home/py3env/Blog/media>
	      Require all granted
	    </Directory>


	#    <Directory /home/py3env/ERP/dms/media>
	#      Require all granted
	#    </Directory>

	#    <Directory /home/py3env/ERP/dms/static>
	#      Require all granted
	#    </Directory>
	    
	#     <Directory /home/py3env/ERP/dms/templates>
	#      Require all granted
	#    </Directory>




	    WSGIDaemonProcess localhost python-path=/home/py3env/ERP:/home/py3env/lib/python3.4/site-packages
	    WSGIProcessGroup localhost

	    WSGIScriptAlias / /home/py3env/Blog/Blog/wsgi.py
	    <Directory /home/py3env/Blog/Blog>
	    <Files wsgi.py>
	     Require all granted
	    </Files>
	    </Directory>
	myproject wsig config
	import os
	from django.core.wsgi import get_wsgi_application
	from os.path import join,dirname,abspath
	PROJECT_DIR = dirname(dirname(abspath(__file__)))
	import sys
	sys.path.insert(0,PROJECT_DIR)
	os.environ["DJANGO_SETTINGS_MODULE"]= "Blog.settings"
	application = get_wsgi_application()

	install mod_wsig
	//make clean 
	//yuanma install python3 configure --enable-shared make makeinstall
	sudo apt-get install libapache2-mod-wsgi-py3
	sudo apt-get install apache2

cache缓存。memcached
	首先，由于memcached依赖于libevent，到libevent和memcached 的官网下载安装包，

	 1.libevent-dev memcached
	 然后，安装 python-memcached：
	 2 pip install python-memcached/ sudo apt-get install python-dev/libmemcached-dev pip install pylibmc
	 最后，配置好settings.py里CACHES 的配置项：
	 3 settings
	 CACHES = {
	    'default': {
	        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
	        'LOCATION': '127.0.0.1:11211',
	            #['172.19.26.240:11211',
	            #'172.19.26.242:11211',]
	    			}
					}
	4 并在MIDDLEWARE_CLASSES 里面的最前面加上：
	             'django.middleware.cache.UpdateCacheMiddleware',
	  在最后面加上：
	             'django.middleware.cache.FetchFromCacheMiddleware',	



11.views
	class-based-views
		ListView
			from django.views.generic import ListView
			
			class PostListView(ListView):
				queryset = Post.published.all()
				context_object_name = 'posts'
				paginate_by = 3
				template_name = 'blog/post/list.html'
			urls.py
				views.PostListView.as_view() 


12.mail
	•	 EMAIL_HOST : The SMTP server host. Default localhost .
	•	 EMAIL_PORT : The SMTP port Default 25.
	•	 EMAIL_HOST_USER : Username for the SMTP server.
	•	 EMAIL_HOST_PASSWORD : Password for the SMTP server.
	•	 EMAIL_USE_TLS : Whether to use a TLS secure connection.
	•	 EMAIL_USE_SSL : Whether to use an implicit TLS secure connection.
	#mail settings
	EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'

	EMAIL_USE_TLS = False
	EMAIL_HOST = 'smtp.163.com'
	EMAIL_PORT = 25
	EMAIL_HOST_USER = 'kongxiuzhi@163.com'
	EMAIL_HOST_PASSWORD = '163smtp'
	DEFAULT_FROM_EMAIL = 'kongxiuzhi@163.com'

	#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
	from django.core.mail import send_mail
    send_mail() takes the subject, message, sender, and list of recipients as required
	arguments.
	send_mail()

13.custom template tags and filters
	Django provides the following helper functions that allow you to create your own
	template tags in an easy manner:
	•	 simple_tag : Processes the data and returns a string
	•	 inclusion_tag : Processes the data and returns a rendered template
	•	 assignment_tag : Processes the data and sets a variable in the context

	Inside your blog application directory, create a new directory, name it
	templatetags and add an empty __init__.py file to it. Create another file in the
	same folder and name it blog_tags.py . The file structure of the blog application
	should look like the following:
		blog/
			__init__.py
			models.py
			...
			templatetags/
				__init__.py
				blog_tags.py #The name of the file is important. You are going to use the name of this module to  load your tags in templates.
		#edit blog_tags.py
		from django import template
		register = template.Library()
		from ..models import Post
		@register.simple_tag#@register.simple_tag(name='my_tag') 自定义tags名字
		def total_posts():
			return Post.published.count()
		#在template中
		{% load blog_tags %}
		{% load staticfiles %}
		...
		<p>...{% total_posts %}...</p>
		#edit blog_tags.py
		@register.inclusion_tag('blog/post/latest_posts.html')
		def show_latest_posts(count=5):#使用方法{% show_latest_posts 3 %}
			latest_posts = Post.published.order_by('-publish')[:count]
			return {'latest_posts': latest_posts}
		#创建latest_posts.html
		<ul>
			{% for post in latest_posts %}
			<li>
			<a href="{{ post.get_absolute_url }}">{{ post.title }}</a>
			</li>
			{% endfor %}
		</ul>
		#edit blog_tags.py
		from django.db.models import Count
		@register.assignment_tag
		def get_most_commented_posts(count=5):
			return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
		#在模版中
		<h3>Most commented posts</h3>
		{% get_most_commented_posts as most_commented_posts %}
		<ul>
		{% for post in most_commented_posts %}
		<li>
		<a href="{{ post.get_absolute_url }}">{{ post.title }}</a>
		</li>
		{% endfor %}
		</ul>
		#creating custom template filter
		#pip install Markdown
		#edit blog_tags.py
		from django.utils.safestring import mark_safe
		import markdown
		@register.filter(name='markdown')
		def markdown_format(text):#{{ post.body|markdown }}
			return mark_safe(markdown.markdown(text))
	
14.custom authentication backend
	from django.contrib.auth.models import User
	class EmailAuthBackend(object):
	"""
	Authenticate using e-mail account.
	"""
		def authenticate(self, username=None, password=None):
			try:
				user = User.objects.get(email=username)
				if user.check_password(password):
					return user
				return None
			except User.DoesNotExist:
				return None
		def get_user(self, user_id):
			try:
				return User.objects.get(pk=user_id)
			except User.DoesNotExist:
				return None

15.Cross-Site Request Forgery in AJAX requests
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/
	jquery.min.js"></script>
	<script src=" http://cdn.jsdelivr.net/jquery.cookie/1.4.1/jquery.
	cookie.min.js "></script>
	<script>
		var csrftoken = $.cookie('csrftoken');
		function csrfSafeMethod(method) {
			// these HTTP methods do not require CSRF protection
			return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
			}
		$.ajaxSetup({
			beforeSend: function(xhr, settings) {
				if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
					xhr.setRequestHeader("X-CSRFToken", csrftoken);
					}	
				}
			});
		$(document).ready(function(){
							{% block domready %}
							{% endblock %}
				});
	</script>


	$.post(url,{json},function(data){})
