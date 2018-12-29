from rest_framework import serializers

time_stamp_fields = ('created', 'modified')
id_fields = ('id', )


class MyChoiceField(serializers.ChoiceField):
    def to_representation(self, value):
        return self._choices.get(value, value)
