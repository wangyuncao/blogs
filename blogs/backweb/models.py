from django.db import models


class Atype(models.Model):
    name = models.CharField(max_length=10)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'atype'


class Permission(models.Model):
    """
    权限表
    文章列表权限 -----> LISTARTICLE
    文章添加权限 -----> ADDARTICLE
    文章编辑权限 -----> EDILARTICLE
    文章删除权限 -----> DELARTICLE
    """
    p_name = models.CharField(max_length=15)

    class Meta:
        db_table = 'permission'


class Role(models.Model):
    """
    角色表
    """
    r_name = models.CharField(max_length=10, unique=True)
    # 每个角色可能有1个或多个权限
    r_p = models.ManyToManyField(Permission)

    class Meta:
        db_table = 'role'


class Article(models.Model):
    # 名字
    a_name = models.CharField(max_length=30, unique=True, null=False)
    # 类别
    a_category = models.ForeignKey(Atype, null=True)
    # 描述
    a_desc = models.CharField(max_length=50, null=True)
    # 内容
    a_content = models.TextField()
    # 是否隐藏
    a_conceal = models.BooleanField(default=False)
    # 是否推荐
    a_recommend = models.BooleanField(default=True)
    # 图片
    image_url = models.ImageField(upload_to='upload', null=True)
    # 点击量
    a_hit = models.IntegerField(default=0)
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True)

    # 数据库表名
    class Meta:
        db_table = 'article'


class User(models.Model):
    # 用户名
    username = models.CharField(max_length=10)
    # 密码
    password = models.CharField(max_length=255)
    # 是否超级用户
    is_superuser = models.BooleanField(default=False)
    # 注册时间
    create_time = models.DateTimeField(auto_now_add=True)
    # session的id
    session_id = models.CharField(max_length=30, null=True)
    # 过期时间
    out_time = models.DateTimeField(null=True)
    # 用户和角色是1对多关系
    u_r = models.ForeignKey(Role, null=True)

    class Meta:
        db_table = 'user'