from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Project, Task, Board, Column
from .serializers import ProjectSerializer, TaskSerializer, BoardSerializer, ColumnSerializer

class ProjectView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        projects = Project.objects.filter(owner=request.user)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = ProjectSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=400)
    
class TaskView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        project_id = request.query_params.get('project_id')

        tasks = Task.objects.filter(project_id=project_id)
        serializer = TaskSerializer(tasks, many = True)

        return Response(serializer.data)
    
    def post(self,request):
        serializer = TaskSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(assigned_to=request.user)
            return Response(serializer.data,status=201)
        
        return Response(serializer.errors, status=400)
    
class BoardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        boards = Board.objects.filter(project__owner=request.user)
        serializer = BoardSerializer(boards, many =True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = BoardSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status=400)
    
class ColumnView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        board_id = request.query_params.get('board_id')
        columns = Column.objects.filter(board_id=board_id)
        serializer = ColumnSerializer(columns, many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = ColumnSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status=400)

class MoveTaskView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id, project__owner=request.user)
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=404)
        
        column_id = request.data.get("column_id")
        order = request.data.get("order")

        try:
            column = Column.objects.get(id=column_id)
        except Column.DoesNotExist:
            return Response({"error": "Column not found"}, status=404)
        
        task.column = column
        task.order = order
        task.save()

        return Response({"message": "Task moved successfully"})
    
class ReorderTasksView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        tasks_data = request.data.get("tasks", [])

        for task_item in tasks_data:
            try:
                task = Task.objects.get(id=task_item["id"], project__owner=request.user)
            except Task.DoesNotExist:
                return Response({"error": f"Task {task_item['id']} not found"}, status=404)
            
            try:
                column = Column.objects.get(id=task_item["column_id"], board__project__owner=request.user)
            except Column.DoesNotExist:
                return Response({"error": f"Column {task_item['column_id']} not found"}, status=400)
            
            task.order = task_item["order"]
            task.column_id = task_item["column_id"]
            task.save()

        return Response({"message": "Tasks reordered succesfully"})    