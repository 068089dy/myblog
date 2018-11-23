# from django.contrib.auth.models import User, Group
from rest_framework import serializers


# 工厂模式实现在视图中自定义序列化类
class FactorySerializer(serializers.ModelSerializer):

    @classmethod
    def get_serializer(cls, attr_model, attr_field='__all__', attr_exclude=()):
        class Meta:
            model = attr_model
            if attr_exclude:
                exclude = attr_exclude
            else:
                fields = attr_field
            depth = 1
        attrs = {
            '__module__': cls.__module__,
            'Meta': Meta
        }
        return type(attr_model.__name__+'Serializer', (cls,), attrs)


