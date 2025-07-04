# board/models.py

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Board(models.Model):
    # 제목: 최대 200자까지 저장 가능한 문자열 필드
    title = models.CharField(max_length=200)

    # 작성자: 작성 유저
    writer = models.ForeignKey(User, on_delete=models.CASCADE)

    # 내용: 글자 수 제한이 없는 긴 텍스트 필드
    content = models.TextField()

    # 등록일: 날짜와 시간을 자동으로 저장. auto_now_add=True는 객체가 처음 생성될 때의 날짜/시간을 저장합니다.
    # 영상의 regdate, regtime을 합친 역할입니다.
    regdate = models.DateTimeField(auto_now_add=True)

    # 조회수: 0 이상의 정수만 저장 가능하며, 기본값은 0입니다.
    readcount = models.IntegerField(default=0)

    # 관리자 페이지 등에서 객체를 문자열로 표시할 때 사용 (게시글 제목이 보이도록 설정)
    def __str__(self):
        return self.title

    # 조회수를 1 증가시키는 메서드
    def increment_read_count(self):
        self.readcount += 1
        self.save()
