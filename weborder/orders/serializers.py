from rest_framework import serializers
from .models import UserProfile, Attachment, Order


class UserProfileSerializer(serializers.ModelSerializer):
    age = serializers.ReadOnlyField()

    def update(self, instance, validated_data):
        validated_data.pop('phone', None)  # Удаляем номер телефона из данных для обновления
        return super(UserProfileSerializer, self).update(instance, validated_data)

    class Meta:
        model = UserProfile
        fields = ('id', 'phone', 'birth_date', 'age', 'photo', 'date_joined', 'is_active', 'is_staff')


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = UserProfile
        fields = ['phone', 'birth_date', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = UserProfile(
            phone=self.validated_data['phone'],
            birth_date=self.validated_data['birth_date']
        )
        if user.age < 18:
            raise serializers.ValidationError({'birth_date': 'Users younger than 18 are not allowed.'})
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user

class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        attachments_data = validated_data.pop('attachments', [])
        order = Order.objects.create(**validated_data)
        for attachment_data in attachments_data:
            Attachment.objects.create(order=order, **attachment_data)
        return order
