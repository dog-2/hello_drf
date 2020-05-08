from rest_framework.serializers import ModelSerializer, CharField, ListSerializer
from rest_framework.exceptions import ValidationError
from . import models

# 可以单独作为Publish接口的序列化类，也可以作为Book序列化外键publish辅助的序列化组件
class PublishModelSerializer(ModelSerializer):
    class Meta:
        model = models.Publish
        fields = ('name', 'address')

class BookModelSerializer(ModelSerializer):
    class Meta:
        model = models.Book
        fields = ('name', 'price', 'publish', 'authors')
    def validate_name(self, value):
        print(self.context.get('request').method)  #序列化层接收参数
        return value