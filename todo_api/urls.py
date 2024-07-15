from django.urls import path
# from .views import CreateTodoAPIView, ListTodoAPIView
from .views import TodosAPIView, TodoDetailAPIView

urlpatterns = [
    path("", TodosAPIView.as_view(), name="todos"),
    path("<int:id>", TodoDetailAPIView.as_view(), name="todo")
    # path("create", CreateTodoAPIView.as_view(), name="create-todo"),
    # path("list", ListTodoAPIView.as_view(), name="list-todo"),
]