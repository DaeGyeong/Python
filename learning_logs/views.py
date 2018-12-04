from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry, Comment
from .forms import TopicForm, EntryForm, CommentForm

# Create your views here.

def index(request):
    ''' home page '''
    return render(request, 'learning_logs/index.html')

def mon(request):
    url = "http://api.nsight.navercorp.com/monapi/api/request?r=R-20150923-001&k=dev-cloudojt001-ncl&rt=img"
    return render(request, 'learning_logs/mon.html', {'url': url})

@login_required
def topics(request):
    ''' 주제를 모두 표시 '''
    #topics = Topic.objects.order_by('date_added')  # 모든 사용자 접근가능
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')  # 필터를 거쳐 로그인한 사용자만 접근 가능

    context = {'topics' : topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    ''' 주제 하나와 연결된 모든 항목을 표시 '''
    topic = Topic.objects.get(id=topic_id)

    if topic.owner != request.user: # 주제가 현재 사용자의 것인지 확인
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    ''' 새 주제 추가 '''
    if request.method != 'POST':
        # 들어온 데이터가 없을 때는 새 폼을 만듭니다.
        form = TopicForm()
    else:
        # POST 데이터를 받아서 처리
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            #form.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    ''' 특정 주제에 관한 새 항목을 추가 '''
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        #전송된 데이터가 없으므로 빈 폼 생성
        form = EntryForm()
    else :
        # 받은 데이터를 POST 처리
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))

    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    ''' 기존항목 편집 '''
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http4Http404

    if request.method != 'POST':
        # 첫 요청이므로 폼을 현재 텍스트로 채움
        form = EntryForm(instance=entry)
    else :
        # POST 데이터를 받았을때 받은 데이터 처리
        form = EntryForm(instance = entry, data = request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)


@login_required
def entry_delete(request, entry_id, topic_id):
    entry = Entry.objects.get(id=entry_id)
    entry.delete()
    topic = Topic.objects.get(id=topic_id)

    if topic.owner != request.user: # 주제가 현재 사용자의 것인지 확인
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    #return render(request, 'learning_logs/topic.html', context)
    return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))


# 추가
def add_comment(request, topic_id, entry_id):
    post = Entry.objects.get(id=entry_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            #return redirect('learning_logs.views.topics', pk=post.pk)
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))
    else:
        form = CommentForm()
    return render(request, 'learning_logs/add_comment.html', {'form': form})


# 삭제 버튼 구현
def comment_delete(request, topic_id, comment_id):
    entry = Comment.objects.get(id=comment_id)
    entry.delete()

    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}

    return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))

# 수정
def edit_comment(request, topic_id, entry_id, comment_id):
    entry = Entry.objects.get(id=entry_id)
    comment = Comment.objects.get(id=comment_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http4Http404

    if request.method != 'POST':
        # 첫 요청이므로 폼을 현재 텍스트로 채움
        form = CommentForm(instance=comment)
    else :
        # POST 데이터를 받았을때 받은 데이터 처리
        form = CommentForm(instance = comment, data = request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))

    context = {'comment': comment, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_comment.html', context)
