from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def logout_view(request):
    ''' 로그 아웃 '''
    logout(request)
    print("Logout\n\n\n\n")
    return HttpResponseRedirect(reverse('learning_logs:index'))

def register(request):
    ''' 새 사용자 등록 '''
    if request.method != 'POST':
        # 빈 등록 폼을 표시
        form = UserCreationForm()
        print("새로 생성\n\n\n\n\n")
    else:
        # 전송 받은 폼을 처리
        form = UserCreationForm(data=request.POST)


        if form.is_valid():
            new_user = form.save()
            # 새 사용자를 로그인 시키고 홈페이지로 리다이렉트 시킴
            authenticated_user = authenticate(username=new_user.username, password=request.POST['password1'])
            login(request, authenticated_user)
            print("생성된놈 로그인\n\n\n\n")
            return HttpResponseRedirect(reverse('learning_logs:index'))

    context = {'form': form}
    return render(request, 'users/register.html', context)
