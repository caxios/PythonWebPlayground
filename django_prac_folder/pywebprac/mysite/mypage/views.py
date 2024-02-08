from django.shortcuts import render

# Create your views here.
def mypageView(request):
    return render(request, template_name='mypage/mypage.html')