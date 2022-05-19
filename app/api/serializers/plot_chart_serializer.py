from rest_framework import fields, serializers
from customadmin.models import PersonalChart


class PersonalChartSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    date_of_birth = serializers.DateField(required=True)
    class Meta:
        model = PersonalChart
        fields = ['id', 'name', 'date_of_birth']

    def create(self, validated_data):
        data_exists = PersonalChart.objects.filter(name=validated_data['name'], date_of_birth=validated_data['date_of_birth'])
        if not data_exists:
            PersonalChart.objects.create(name=validated_data['name'], date_of_birth=validated_data['date_of_birth'])
        return validated_data
