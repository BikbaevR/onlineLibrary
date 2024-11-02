from django.contrib import admin
from .models import *

admin.site.register(
    [
        UserTag,
        CustomUser,
        Genre,
        Book,
        Comment,
        Favorite,
        UserHistory,
        Statistic
    ]
)
