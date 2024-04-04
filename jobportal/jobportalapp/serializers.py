from rest_framework import serializers
from jobportalapp.models import User, PersonalInfo, Education, Experience, Skill, Profile
from xml.dom import ValidationErr
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class UserRegistrationSerializer(serializers.ModelSerializer):
    password=serializers.CharField(style={'input_type':'password'})
    # password2=serializers.CharField(style={'input_type':'password'},write_only=True)

    class Meta:
        model=User
        fields = ['email','name','password']
        # extra_kwargs={
        #     'password':{'write_only':True}
        # }

    #validating password and confirm password while registration
     
    # def validate(self,attrs):
    #     password=attrs.get('password')
        # password2=attrs.get('password2')

        # if password != password2:
        #     raise serializers.ValidationError("password and confrim password does not match")
        # return attrs

    def save(self,**kwargs):
        # print('hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh',data)
        password = self.validated_data.pop('password')
        user = User.objects.create(**self.validated_data)
        user.set_password(password)
        user.save()
        return user
        
    
class UserLoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=250)
    class Meta:
        model= User
        fields=['email','password']


class UserPersonalInfoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=PersonalInfo
        fields='__all__'

class UserEducationSerializer(serializers.ModelSerializer):
      class Meta:
       model = Education
       fields= ['education','board','passing_out_year','total_marks']

class UserExperienceSerializer(serializers.ModelSerializer):
      class Meta:
       model = Experience
       fields='__all__'


class UserSkillsSerializer(serializers.ModelSerializer):
      class Meta:
        model = Skill
        fields='__all__'


class UserProfileSerializer(serializers.ModelSerializer):
        class Meta:
          model = Profile
          fields = "__all__"