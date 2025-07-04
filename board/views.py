from django.shortcuts import render, get_object_or_404, redirect
from .models import Board


def index(request):
    # templates/board/index.html 파일을 화면에 렌더링(표시)합니다.
    return render(request, "board/index.html")


def list(request):
    # Board 모델의 모든 객체를 id의 내림차순(-id)으로 정렬하여 가져옴
    board_list = Board.objects.order_by("-id")
    # 템플릿으로 전달할 데이터를 context 딕셔너리로 만듦
    context = {"board_list": board_list}
    # list.html을 렌더링하면서 context 데이터를 함께 전달
    return render(request, "board/list.html", context)


def read(request, id):
    # id 값으로 특정 Board 객체를 찾습니다. 만약 객체가 없으면 404 오류를 발생시킵니다.
    board = get_object_or_404(Board, id=id)
    # 3단계에서 모델에 만들었던 조회수 증가 메서드를 호출합니다.
    board.increment_read_count()

    context = {"board": board}
    return render(request, "board/read.html", context)


def register(request):
    if request.method == "POST":
        # POST 요청일 경우, 폼에서 전송된 데이터로 Board 객체 생성
        board = Board()
        board.title = request.POST["title"]
        board.writer = request.POST["writer"]
        board.content = request.POST["content"]
        # 데이터베이스에 저장
        board.save()
        # 저장 후에는 게시글 목록 페이지로 이동시킴
        return redirect("board:list")
    else:
        # GET 요청일 경우, 비어있는 등록 페이지(register.html)를 보여줌
        return render(request, "board/register.html")


def edit(request, id):
    # id 값으로 수정할 게시글 객체를 가져옴
    board = get_object_or_404(Board, id=id)

    if request.method == "POST":
        # POST 요청일 경우, 폼 데이터로 기존 객체의 내용을 수정
        board.title = request.POST["title"]
        # 작성자는 수정하지 않음
        board.content = request.POST["content"]
        board.save()
        # 수정이 완료되면 해당 글의 상세 보기 페이지로 이동
        return redirect("board:read", id=board.id)
    else:
        # GET 요청일 경우, 기존 데이터가 채워진 수정 페이지를 보여줌
        context = {"board": board}
        return render(request, "board/edit.html", context)


def remove(request, id):
    # id 값으로 특정 Board 객체를 찾습니다. 만약 객체가 없으면 404 오류를 발생시킵니다.
    board = get_object_or_404(Board, id=id)

    if request.method == "POST":
        # POST 요청일 경우, 객체를 데이터베이스에서 삭제
        board.delete()
        # 삭제 후에는 목록 페이지로 이동
        return redirect("board:list")
    else:
        # GET 요청일 경우, 삭제 확인 페이지를 보여줌
        context = {"board": board}
        return render(request, "board/remove.html", context)
