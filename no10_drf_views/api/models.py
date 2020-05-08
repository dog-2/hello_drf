from django.db import models

# 基类
class BaseModel(models.Model):
    is_delete = models.BooleanField(default=False)  # 默认不是删除，数据库中是0/1
    create_time = models.DateTimeField(auto_now_add=True)

    # 设置 abstract = True 来声明基表，作为基表的Model不能在数据库中形成对应的表
    class Meta:
        abstract = True  # 声明该表只是一个抽象表不出现在数据库中

# 书籍表
class Book(BaseModel):
    name = models.CharField(max_length=64, blank=False)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    img = models.ImageField(upload_to='img', default='default.jpg')
    # 关联出版社表
    publish = models.ForeignKey(
        to='Publish',  # 关联publish表
        db_constraint=False,  # 断关联（断开Book表和Publish表的关联,方便删数据,虽然断开了关联但是还能正常使用）
        related_name='books',  # 反向查询字段：publish_obj.books就能查出当前出版社出版的的所有书籍
        on_delete=models.DO_NOTHING,  # 设置连表操作关系
        blank=False,
    )
    # 关联作者表
    authors = models.ManyToManyField(
        to='Author',
        db_constraint=False,  # 断开关联
        related_name='books',  # 反向查询字段
    )

    # 序列化插拔式属性 - 完成自定义字段名完成连表查询
    @property
    def publish_name(self):  # 自定义查询出版社名字
        return self.publish.name

    @property
    def author_list(self):
        return self.authors.values('name', 'age', 'detail__mobile').all()

    class Meta:
        db_table = 'book'
        verbose_name = '书籍'
        verbose_name_plural = verbose_name

        unique_together = ('name', 'publish')

    def __str__(self):
        return self.name

# 出版社表
class Publish(BaseModel):
    """name、address、is_delete、create_time"""
    name = models.CharField(max_length=64)
    address = models.CharField(max_length=64)

    class Meta:
        db_table = 'publish'
        verbose_name = '出版社'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# 作者表
class Author(BaseModel):
    """name、age、is_delete、create_time"""
    name = models.CharField(max_length=64)
    age = models.IntegerField()

    class Meta:
        db_table = 'author'
        verbose_name = '作者'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# 作者详情
class AuthorDetail(BaseModel):
    """mobile, author、is_delete、create_time"""
    mobile = models.CharField(max_length=11)
    author = models.OneToOneField(
        to='Author',
        db_constraint=False,
        related_name='detail',
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'author_detail'
        verbose_name = '作者详情'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.author.name
