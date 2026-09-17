from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from tasks.models import Task

from .models import Comment
from .serializers import CommentCreateSerializer, CommentSerializer


class CommentListCreateView(APIView):
  

    permission_classes = [IsAuthenticated]

    def get_task(self, task_id):
        try:
            return Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            return None

    def get(self, request, task_id):
        task = self.get_task(task_id)
        if not task:
            return Response({"detail": "Task not found."}, status=status.HTTP_404_NOT_FOUND)

        comments = Comment.objects.filter(task=task).select_related("user")
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, task_id):
        task = self.get_task(task_id)
        if not task:
            return Response({"detail": "Task not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save(task=task, user=request.user)

        return Response(
            CommentSerializer(comment).data,
            status=status.HTTP_201_CREATED,
        )


class CommentDeleteView(APIView):


    permission_classes = [IsAuthenticated]

    def delete(self, request, task_id, comment_id):
        try:
            comment = Comment.objects.get(pk=comment_id, task_id=task_id)
        except Comment.DoesNotExist:
            return Response({"detail": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)

        # Only the owner or an admin can delete
        if comment.user != request.user and not request.user.is_staff:
            return Response(
                {"detail": "You do not have permission to delete this comment."},
                status=status.HTTP_403_FORBIDDEN,
            )

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
