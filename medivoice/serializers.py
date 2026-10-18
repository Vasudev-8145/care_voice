
from rest_framework import serializers

from django.contrib.auth.models import User

from medivoice.models import Complaint

class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User

        fields = ["id","username","first_name","last_name","email","password"]

        read_only_fields = ["id"]

class ComplaintSerializer(serializers.ModelSerializer):

    owner = serializers.StringRelatedField()

    class Meta:

        model = Complaint

        fields = "__all__"

        read_only_fields = ["id","reported_date","owner"]

    def validate(self,validated_data):

        title = validated_data.get("title")
        description = validated_data.get("description")

        if not title or not title.strip():

            raise serializers.ValidationError("title field can't be null")

        if not description or not description.strip():

            raise serializers.ValidationError("description field can't be null")

        return validated_data

        