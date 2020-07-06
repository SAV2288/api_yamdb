from rest_framework import viewsets, exceptions
from rest_framework.generics import get_object_or_404

from api.models import Review, Comment, Rate, Title
from api.serializers import ReviewSerializer, CommentSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def perform_create(self, serializer):

        try:
            title = get_object_or_404(Title, pk=self.kwargs['title_id'])
            Review.objects.get(title=title, author=self.request.user)
        except Exception:
            raise exceptions.ValidationError('You have already made a review ')

        serializer.save(author=self.request.user)

        score = Rate.objects.get(title=title)
        score.rate_update(score=self.request.data.get('score'))

    
    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        return Review.objects.filter(title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    # permission_classes = [
    #     permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly
    # ]

    def get_queryset(self):
        return Comment.objects.filter(title=self.kwargs.get('title_id'),
                                      review_id=self.kwargs.get('review_id'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
