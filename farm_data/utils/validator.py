from rest_framework import serializers

def validate_range(value: int, min_value: int, max_value: int, field_name: str) -> int:
    if value < min_value or value > max_value:
        raise serializers.ValidationError(f'{field_name} must be between {min_value} and {max_value}')
    return value

def validate_non_negative(value: int, field_name: str)-> int:
    if value < 0:
        raise serializers.ValidationError(f'{field_name} cannot be negative.')
    return value