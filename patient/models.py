from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.CharField(max_length=200, default='')
    image = models.ImageField(upload_to="user_image/Post")
    dateOFpost = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.user) + ' '+ str(self.dateOFpost.date())

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    userImage = models.ImageField(upload_to="user_image/Profiles", default="user_image/default/default.jpg")
    bio = models.CharField(max_length=200, blank=True)
    follower = models.IntegerField(default = 0)
    following = models.IntegerField(default=0)


    def __str__(self):
        return str(self.user)


class T_View(models.Model):
    user = models.ManyToManyField(User, related_name="viewingUser")
    post = models.OneToOneField(Post, on_delete=models.CASCADE)

    @classmethod
    def viewed(cls, post, viewing_user):
        obj, create = cls.objects.get_or_create(post = post)
        obj.user.add(viewing_user)

    @classmethod
    def ignore(cls, post, ignoring_user):
        obj, create = cls.objects.get_or_create(post=post)
        obj.user.remove(ignoring_user)
    
    def __str__(self):
        return str(self.post)

class Following(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followed = models.ManyToManyField(User, related_name="followed")
    follower = models.ManyToManyField(User, related_name="follower")

    @classmethod
    def follow(cls, user, another_account):
        obj, create = cls.objects.get_or_create(user = user)
        obj.followed.add(another_account)
    
    @classmethod
    def unfollow(cls, user, another_account):
        obj, create = cls.objects.get_or_create(user=user)
        obj.followed.remove(another_account)

    def __str__(self):
        return str(self.user)
    
