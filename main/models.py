from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = (
        ('writer', 'Writer'),
        ('client', 'Client'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20)
    phone = models.CharField(max_length=15, blank=True)
    bio = models.TextField(blank=True, null=True)
    skills = models.CharField(max_length=200, blank=True, null=True)
    experience = models.CharField(max_length=100, blank=True, null=True)

    profile_image = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.username
    
class HireRequest(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    message = models.TextField(blank=True)
    status = models.CharField(max_length=10, default='pending')
    def __str__(self):
        return f"{self.client} -> {self.writer}"

# =========================
# ARTICLE MODEL 
# =========================
class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)    
    name = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='articles/', null=True, blank=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()

    def __str__(self):
        return self.text[:30]


# =========================
# BLOG MODEL
# =========================
class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='blogs/', null=True, blank=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class BlogComment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()

    def __str__(self):
        return self.text[:30]


# =========================
# CONTENT MODEL
# =========================
class Content(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='contents/', null=True, blank=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class ContentComment(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()

    def __str__(self):
        return self.text[:30]
    
class Chat(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_chats')
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='writer_chats')
    

    def __str__(self):
        return f"{self.client} - {self.writer}"


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

class HireRequest(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')

    status = models.CharField(max_length=10, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ], default='pending')

    created_at = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    
    rating = models.IntegerField()  # 1 to 5
    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.writer.username} - {self.rating}"