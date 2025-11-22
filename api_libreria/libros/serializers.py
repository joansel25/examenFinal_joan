from rest_framework import serializers
from .models import Libro

class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = '__all__'
        read_only_fields = ['id']
        
    def validate_stock(self, value):
        if value <0:
            raise serializers.ValidationError("El stock no puede ser negativo")
        return value
    def validate_isbn(self, value):
        if value and len(value) != 13:
            raise serializers.ValidationError("El isbn debe tener exactamente 13 caracteres")
        return value