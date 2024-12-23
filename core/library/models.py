from django.contrib.auth.models import AbstractUser
from django.db import models



class UserTag(models.Model):
    tag_name = models.CharField(max_length=50)

    def __str__(self):
        return self.tag_name


class CustomUser(AbstractUser):
    money = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tag = models.ManyToManyField(UserTag, blank=True)
    user_image = models.ImageField(upload_to='user_images', blank=True)
    is_email_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=64, blank=True, null=True)


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    year = models.IntegerField()
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='books/img', blank=False, null=False)
    rating = models.IntegerField()
    pages = models.IntegerField()
    genres = models.ManyToManyField(Genre)
    file = models.FileField(upload_to='books/files', null=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    comment = models.TextField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.user.username}: {self.comment[:20]}..."


class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.book.title}'


class UserHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.book.title}'


class Statistic(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    shopping = models.IntegerField()
    comments = models.IntegerField()
    favorites = models.IntegerField()

    def __str__(self):
        return f'{self.user.name}'


class TopUpHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    card_number = models.IntegerField()
    datetime = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.user.username}'
