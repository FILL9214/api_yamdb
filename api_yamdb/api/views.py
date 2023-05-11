from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from serializers import CommentSerializer, ReviewSerializer
from reviews.models import Review, Title

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    # permission_classes = 
    # Аноним может читать все комменты
    # Аутентифицированный пользователь = Аноним + может писать свой + может менять свой + может удалять свой 
    # Модератор = Аутифицированный + права аутиф. для чужих комментов
    


    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    # permission_classes = 
    

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)