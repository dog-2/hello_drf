# 序列化组件 - 为每一个model类通过一套序列化工具类
# 序列化组件的工作方式与django froms组件非常相似
from rest_framework import serializers, exceptions
from django.conf import settings
from . import models

class UserSerializer(serializers.Serializer):   #创建一个序列化类
    name = serializers.CharField()      
    phone = serializers.CharField()
    # 序列化提供给前台的字段个数由后台决定，可以少提供，但是提供的数据库对应的字段，名字一定要与数据库字段相同
    sex = serializers.IntegerField()
    icon = serializers.ImageField()

    # 自定义序列化属性
    # 属性名随意，值由固定的命名规范方法提供:
    #       get_属性名(self, 参与序列化的model对象)
    #       返回值就是自定义序列化属性的值
    gender = serializers.SerializerMethodField()
    def get_gender(self, obj):
        # choice类型的解释型值 get_字段_display() 来访问
        return obj.get_sex_display()

    #自定义序列化属性icon
    icon = serializers.SerializerMethodField()
    def get_icon(self, obj):
        # settings.MEDIA_URL: 自己配置的 /media/，给后面高级序列化与视图类准备的
        # obj.icon不能直接作为数据返回，因为内容虽然是字符串，但是类型是ImageFieldFile类型
        return '%s%s%s' % (r'http://127.0.0.1:8000', settings.MEDIA_URL, str(obj.icon))
    
class UserDeserializer(serializers.Serializer):
    # 1) 哪些字段必须反序列化
    # 2) 字段都有哪些安全校验
    # 3) 哪些字段需要额外提供校验  钩子函数
    # 4) 哪些字段间存在联合校验
    # 注：反序列化字段都是用来入库的，不会出现自定义方法属性，会出现可以设置校验规则的自定义属性,不入数据库的
    name = serializers.CharField(
        max_length=64,
        min_length=3,
        error_messages={
            'max_length': '太长',
            'min_length': '太短'
        }
    )
    pwd = serializers.CharField()
    phone = serializers.CharField(required=False)
    sex = serializers.IntegerField(required=False)

    # 自定义有校验规则的反序列化字段,例如确认密码字段re_pwd
    re_pwd = serializers.CharField(required=True)

    # 小结：
    # name，pwd，re_pwd为必填字段
    # phone，sex为选填字段
    # 五个字段都必须提供完成的校验规则


    # 局部钩子：validate_要校验的字段名(self, 当前要校验字段的值)
    # 校验规则：校验通过返回原值，校验失败，抛出异常
    def validate_name(self, value):
        if 'g' in value.lower():  # 名字中不能出现g
            raise exceptions.ValidationError('名字非法，是个鸡贼！')
        return value

    # 全局钩子：validate(self, 通过系统与局部钩子校验之后的所有数据)
    # 校验规则：校验通过返回原值，校验失败，抛出异常
    def validate(self, attrs):    #attrs是字典格式
        pwd = attrs.get('pwd')
        re_pwd = attrs.pop('re_pwd')     #因为re_pwd不需要入数据库，所以在全局钩子校验中删除掉这个字段
        if pwd != re_pwd:
            raise exceptions.ValidationError({'pwd&re_pwd': '两次密码不一致'})
        return attrs

    # 要完成新增，必须自己重写 create 方法，validated_data是校验的数据
    def create(self, validated_data):
        # 尽量在所有校验规则完毕之后，数据可以直接入库
        return models.User.objects.create(**validated_data)