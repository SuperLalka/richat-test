from rest_framework import serializers

from app.items.models import Item


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = '__all__'


class RetrieveItemSerializer(ItemSerializer):
    pass


class CreateItemSerializer(ItemSerializer):
    pass
