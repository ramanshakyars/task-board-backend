from django.urls import re_path
from .views import CommentDeleteView, CommentListCreateView

urlpatterns = [
    re_path(
        r"^/?tasks/(?P<task_id>\d+)/comments/?$",
        CommentListCreateView.as_view(),
        name="comment-list-create",
    ),
    re_path(
        r"^/?tasks/(?P<task_id>\d+)/comments/(?P<comment_id>\d+)/?$",
        CommentDeleteView.as_view(),
        name="comment-delete",
    ),
]
