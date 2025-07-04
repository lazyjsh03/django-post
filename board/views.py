from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Board
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required


def index(request):
    # templates/board/index.html 파일을 화면에 렌더링(표시)합니다.
    return render(request, "board/index.html")


def list(request):
    # 1. 모든 게시글을 최신순으로 가져옵니다.
    all_boards = Board.objects.order_by("-id")

    # 2. 사용자가 요청한 페이지 번호를 가져옵니다.
    #    URL에 page 파라미터가 없으면 기본값으로 '1'을 사용합니다.
    page = request.GET.get("page", "1")

    # 3. Paginator 객체를 생성합니다.
    #    (전체 게시글, 한 페이지에 보여줄 게시글 수)
    paginator = Paginator(all_boards, 10)

    # 4. 사용자가 요청한 페이지에 해당하는 게시글 목록을 가져옵니다.
    #    get_page 메서드는 페이지 번호가 잘못되었을 때의 예외 처리를 자동으로 해줍니다.
    page_obj = paginator.get_page(page)

    # 5. 템플릿에 전달할 context 데이터를 수정합니다.
    #    이제 전체 리스트 대신, 해당 페이지의 게시글 목록(page_obj)을 전달합니다.
    context = {"board_list": page_obj}
    return render(request, "board/list.html", context)


def read(request, id):
    # id 값으로 특정 Board 객체를 찾습니다. 만약 객체가 없으면 404 오류를 발생시킵니다.
    board = get_object_or_404(Board, id=id)
    # 3단계에서 모델에 만들었던 조회수 증가 메서드를 호출합니다.
    board.increment_read_count()

    context = {"board": board}
    return render(request, "board/read.html", context)


@login_required(login_url="login")
def register(request):
    if request.method == "POST":
        # POST 요청일 경우, 폼에서 전송된 데이터로 Board 객체 생성
        board = Board()
        board.title = request.POST["title"]
        board.writer = request.user
        board.content = request.POST["content"]
        # 데이터베이스에 저장
        board.save()
        # 저장 후에는 게시글 목록 페이지로 이동시킴
        return redirect("board:list")
    else:
        # GET 요청일 경우, 비어있는 등록 페이지(register.html)를 보여줌
        return render(request, "board/register.html")


@login_required(login_url="login")
def edit(request, id):
    # id 값으로 수정할 게시글 객체를 가져옴
    board = get_object_or_404(Board, id=id)

    # 작성자와 로그인한 유저가 다르면, 목록 페이지로 돌려보냄
    if board.writer != request.user:
        return redirect("board:list")

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


@login_required(login_url="login")
def remove(request, id):
    # id 값으로 특정 Board 객체를 찾습니다. 만약 객체가 없으면 404 오류를 발생시킵니다.
    board = get_object_or_404(Board, id=id)

    # 작성자와 로그인한 유저가 다르면, 목록 페이지로 돌려보냄
    if board.writer != request.user:
        return redirect("board:list")

    if request.method == "POST":
        # POST 요청일 경우, 객체를 데이터베이스에서 삭제
        board.delete()
        # 삭제 후에는 목록 페이지로 이동
        return redirect("board:list")
    else:
        # GET 요청일 경우, 삭제 확인 페이지를 보여줌
        context = {"board": board}
        return render(request, "board/remove.html", context)


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # 사용자를 생성
            login(request, user)  # 생성된 사용자로 바로 로그인
            return redirect("board:list")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})
