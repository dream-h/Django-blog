from django.db import models


class UserInfo(models.Model):
    """
    用户信息表
    """
    nid = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=32, verbose_name='用户名', unique=True)
    password = models.CharField(max_length=64, verbose_name='密码')
    nickname = models.CharField(max_length=64, verbose_name='昵称')
    email = models.EmailField(verbose_name='邮箱', unique=True)
    avatar = models.ImageField(verbose_name='头像', upload_to='avatar/%Y%m%d/', blank=True)
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    fans = models.ManyToManyField(
        verbose_name='粉丝们',
        to='UserInfo',
        through='UserFans',
        related_name='f',
        through_fields=('user', 'follower'),
    )

    def __str__(self):
        return self.username


class Blog(models.Model):
    """
    博客表
    """
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='个人博客标题', max_length=64)
    site = models.CharField(verbose_name='个人博客前缀', max_length=64, unique=True)
    theme = models.CharField(verbose_name='个人博客主题', max_length=32, unique=True)
    user = models.OneToOneField(
        verbose_name='关联用户',
        to='UserInfo',
        to_field='nid',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title


class UserFans(models.Model):
    """
    互粉关系表
    """
    user = models.ForeignKey(verbose_name='博主', to='UserInfo', to_field='nid', related_name='users', on_delete=models.CASCADE)
    follower = models.ForeignKey(verbose_name='粉丝', to='UserInfo', to_field='nid', related_name='followers', on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            ('user', 'follower'),
        ]


class Category(models.Model):
    """
    博主个人文章分类表
    """
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='分类标题', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid', on_delete=models.CASCADE,)

    def __str__(self):
        return self.title


class ArticleDetail(models.Model):
    """
    文章详细表
    """
    content = models.TextField(verbose_name='文章内容')
    article = models.OneToOneField(verbose_name='所属文章', to='Article', to_field='nid', on_delete=models.CASCADE,)

    def __str__(self):
        return self.content


class Tag(models.Model):
    """
    个人文章标签表
    """
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='标签标题', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid', on_delete=models.CASCADE,)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    文章评论表
    """
    nid = models.BigAutoField(primary_key=True)
    content = models.TextField(verbose_name='评论内容')
    created_time = models.DateTimeField(verbose_name='评论时间', auto_now_add=True)

    reply = models.ForeignKey(
        verbose_name='回复评论',
        to='self',
        to_field='nid',
        related_name='back',
        null=True, blank=True,
        on_delete=models.CASCADE,
    )
    article = models.ForeignKey(verbose_name='所属文章', to='Article', to_field='nid', on_delete=models.CASCADE,)
    user = models.ForeignKey(verbose_name='评论者', to='UserInfo', to_field='nid', on_delete=models.CASCADE,)


class UpDown(models.Model):
    """
    文章顶或踩表
    """
    article = models.ForeignKey(verbose_name='所赞文章', to='Article', to_field='nid', on_delete=models.CASCADE,)
    user = models.ForeignKey(verbose_name='赞或踩用户', to='UserInfo', to_field='nid', on_delete=models.CASCADE,)
    up = models.BooleanField(verbose_name='是否赞')

    class Meta:
        unique_together = [
            ('article', 'user'),
        ]


class Article(models.Model):
    """
    文章表
    """

    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='文章标题', max_length=64)
    summary = models.CharField(verbose_name='文章简介', max_length=255)
    read_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid', on_delete=models.CASCADE)
    category = models.ForeignKey(
        verbose_name='所属分类',
        to='Category',
        to_field='nid',
        null=True, blank=True,
        on_delete=models.CASCADE,
    )

    type_choice = [
        (1, 'Python'),
        (2, 'Django'),
        (3, 'book'),
        (4, '区块链'),
        (5, '人工智能'),
    ]
    article_type_id = models.IntegerField(choices=type_choice, default=None)

    tags = models.ManyToManyField(
        verbose_name='文章标签',
        to='Tag',
        through='Article2Tag',
        through_fields=('article', 'tag')
    )

    def __str__(self):
        return self.title


class Article2Tag(models.Model):
    article = models.ForeignKey(verbose_name='文章', to='Article', to_field='nid', on_delete=models.CASCADE)
    tag = models.ForeignKey(verbose_name='标签', to='Tag', to_field='nid', on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            ('article', 'tag'),
        ]