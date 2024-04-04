from django.contrib import admin
from jobportalapp.models import User, PersonalInfo, Education, Experience, Skill, Profile
from django.contrib.auth.admin import UserAdmin as Baseadmin

# Register your models here.
class UserModelAdmin(Baseadmin):
    list_display=['id','name','email','is_admin']
    list_filter=['is_admin']
    fieldsets = [
        ("User Credentials", {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["name"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]

    # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "name", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email", "id"]
    filter_horizontal = []

# Now register the new UserAdmin...
admin.site.register(User,UserModelAdmin)
admin.site.register(Profile)
admin.site.register(PersonalInfo)
admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(Skill)

