from django.urls import path
from .views import ProjectView, TaskView, BoardView, ColumnView, MoveTaskView, ReorderTasksView

urlpatterns = [
    path('', ProjectView.as_view()),
    path('tasks/', TaskView.as_view()),
    path('boards/', BoardView.as_view()),
    path('columns/', ColumnView.as_view()),
    path('tasks/move/<int:task_id>/', MoveTaskView.as_view()),
    path('tasks/reorder/', ReorderTasksView.as_view()),
]