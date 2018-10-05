from rest_framework import serializers


class MyChoiceField(serializers.ChoiceField):
    def to_representation(self, value):
        return self._choices.get(value, value)
