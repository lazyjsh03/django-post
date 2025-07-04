from django.urls import path
from . import views

app_name = "board"

urlpatterns = [
    # /board/ 주소로 접속하면 views.py의 index 함수를 호출합니다.
    # name='index'는 이 URL 패턴의 별명입니다.
    path("", views.index, name="index"),
    # /board/list/ 주소와 views.py의 list 함수를 연결
    path("list/", views.list, name="list"),
    # /board/read/<id>/ 주소와 views.py의 read 함수를 연결
    # <int:id>는 숫자(int) 형태의 파라미터를 id라는 변수 이름으로 받겠다는 의미
    path("read/<int:id>/", views.read, name="read"),
    # /board/register/ 주소와 views.py의 register 함수를 연결
    path("register/", views.register, name="register"),
    # /board/edit/<id>/ 주소와 views.py의 edit 함수를 연결
    path("edit/<int:id>/", views.edit, name="edit"),
    # /board/remove/<id>/ 주소와 views.py의 remove 함수를 연결
    path("remove/<int:id>/", views.remove, name="remove"),
    # signup url 추가
    path("signup/", views.signup, name="signup"),
]
