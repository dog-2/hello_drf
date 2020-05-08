from rest_framework.serializers import ModelSerializer, SerializerMethodField, CharField
from rest_framework.exceptions import ValidationError
from . import models

# 可以单独作为Publish接口的序列化类，也可以作为Book序列化外键publish辅助的序列化组件
class PublishModelSerializer(ModelSerializer):
    class Meta:
        model = models.Publish
        fields = ('name', 'address')

# Book接口序列化
class BookModelSerializer(ModelSerializer):
    # 了解: 1.还可以自定义设置序列化字段，但是必须在fields中声明，在fields中写publish_address
    # publish_address = SerializerMethodField()
    # def get_publish_address(self, obj):
    #     return obj.publish.address

    # 2. 自定义连表深度-子序列化方式-该方式不能参与反序列化，使用在序列化和反序列化共存时，不能书写
    publish = PublishModelSerializer()

    class Meta:
        # 序列化类关联的model类
        model = models.Book
        # 参与序列化的字段
        fields = ('name', 'price', 'img', 'author_list', 'publish')

        # 了解知识点
        # 所有字段
        # fields = '__all__'
        # 与fields不共存，exclude排除哪些字段
        # exclude = ('id', 'is_delete', 'create_time')
        # 自动连表深度
        # depth = 1


class BookModelDeserializer(ModelSerializer):
    # 一些只参与反序列化的字段，但是不是与数据库关联的，自定义不入库的反序列化的字段
    # 自定义字段的 read_only属性必须定义在CharField，不能写在下方的extra_kwargs中，否则会被传入models.Book进行反序列化而报错
    re_name = CharField(read_only=True)

    class Meta:
        model = models.Book
        exclude = ['is_delete', 'create_time', 'img']
        # fields = ('name', 'price', 'publish', 'authors','re_name')  #没有默认值的字段必须序列化，为其传值
        # extra_kwargs 用来完成反序列化字段的 系统校验规则
        extra_kwargs = {
            'name': {
                'required': True,  # 设置name字段必填
                'min_length': 1,
                'error_messages': {
                    'required': '必填项',
                    'min_length': '太短',
                },
            },
        }

    # 局部钩子校验单个字段  validate_字段名
    def validate_name(self, value):  # value是字段name的值
        # 书名不能包含 g 字符
        if 'g' in value.lower():
            raise ValidationError('该g书不能出版')
        return value
    # 全局钩子

    def validate(self, attrs):
        publish = attrs.get('publish')  # publish如果是外键字段，这个就是publish对象
        name = attrs.get('name')
        if models.Book.objects.filter(name=name, publish=publish):
            raise ValidationError({'book': '该书已存在'})
        return attrs

    # 注意：ModelSerializer类已经帮我们实现了 create 与 update 方法,不需要写create就能创建


class V2BookModelSerializer(ModelSerializer):
    # 一些只参与反序列化的字段，但是不是与数据库关联的，自定义不入库的反序列化的字段
    # 自定义字段的 read_only属性必须定义在CharField，不能写在下方的extra_kwargs中，否则会被传入models.Book进行反序列化而报错
    re_name = CharField(read_only=True)

    class Meta:
        model = models.Book
        fields = ('name', 'price', 'img', 'author_list',
                  'publish_name', 'publish', 'authors', 're_name')
        extra_kwargs = {
            'name': {
                'required': True,
                'min_length': 1,
                'error_messages': {
                    'required': '必填项',
                    'min_length': '太短',
                }
            },
            'publish': {
                'write_only': True
            },
            'authors': {
                'write_only': True
            },
            'img': {
                'read_only': True,
            },
            'author_list': {
                'read_only': True,
            },
            'publish_name': {
                'read_only': True,
            }
        }

    def validate_name(self, value):
        # 书名不能包含 g 字符
        if 'g' in value.lower():
            raise ValidationError('该g书不能出版')
        return value

    def validate(self, attrs):
        publish = attrs.get('publish')
        name = attrs.get('name')
        # 视频里使用这种验证方式，实际是不合理的，因为会导致针对价格修改的PUT请求失败(name&publish已存在)
        # 因此在这里将其注释掉 ，正确的方式是在models.Book中对这两个字段的共同唯一性作约束
        # 而本函数通常作为对不同attr的对比验证，如两次输入密码是否一致等
        # if models.Book.objects.filter(name=name, publish=publish):
        #     raise ValidationError({'book': '该书已存在'})
        return attrs
