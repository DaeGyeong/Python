from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Topic(models.Model):
    ''' 사용자가 공부하는 주제 '''
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User)

    def __str__(self):
        ''' 모델에 관한 정보를 문자열 형태로 반환 '''
        return self.text

class Entry(models.Model):
    ''' 주제에 관한 내용 '''
    topic = models.ForeignKey(Topic)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entires'

    def __str__(self):
        if len(self.text) < 10 :
            return self.text
        else :
            return self.text[:10] + "...."


        #return self.text[:20] + "..."
        '''
        if self.text[:20] < 20:
            return self.text[:20] + "..."
        else :
            return self.text
        '''

## 추가
class Comment(models.Model):
    post = models.ForeignKey(Entry, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
