from rest_framework.serializers import ModelSerializer, CharField, ListSerializer
from rest_framework.exceptions import ValidationError
from . import models

# 可以单独作为Publish接口的序列化类，也可以作为Book序列化外键publish辅助的序列化组件
class PublishModelSerializer(ModelSerializer):
    class Meta:
        model = models.Publish
        fields = ('name', 'address')

# 重点：ListSerializer与ModelSerializer建立关联的是： 在ModelSerializer的Meta类中设置   list_serializer_class
class BookListSerializer(ListSerializer):
    def update(self, instance, validated_data):  # print(instance)  # 要更新的对象们
        # print(validated_data)  # 更新的对象对应的数据们
        # print(self.child)  # 服务的模型序列化类 - V3BookModelSerializer
        for index, obj in enumerate(instance):
            self.child.update(obj, validated_data[index])
        return instance


class V3BookModelSerializer(ModelSerializer):
    # 一些只参与反序列化的字段，但是不是与数据库关联的，自定义不入库的反序列化的字段
    # 自定义字段的 read_only属性必须定义在CharField，不能写在下方的extra_kwargs中，否则会被传入models.Book进行反序列化而报错
    re_name = CharField(read_only=True)

    class Meta:
        # 群改，list_serializer_class是固定的key写法，直接转入BookListSerializer类的 update 方法
        list_serializer_class = BookListSerializer
        
        # 由于在models.Book中设置了两个字段的共同unique限定：
        #   unique_together = ('name', 'publish')
        # ListSerializer会为这两个字段添加默认的唯一性验证器 UniqueTogetherValidator，
        # 在群局部修改(PATCH)时，会调用该该验证器，若不同时提供'name'和'publish'的值则报错，
        # 因此若只想提供pk及price做修改则会报错，则不符合默认的业务逻辑。
        # 所以这里将 validators 设置为[]，去掉默认添加的验证器。
        # 而唯一性验证交给数据库层去做。
        validators = []


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
                },
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

