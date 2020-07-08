from django.db.models import Prefetch
from django.template.defaultfilters import slugify

from rest_framework import viewsets, exceptions, filters
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError

from pytils import translit

from api.models import Review, Comment, Rate, Titles, Genres, Categories
from api.serializers import ReviewSerializer, CommentSerializer, GenreSerialiser, CategorySerializer, TitleSerializer


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


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.select_related('category').all().prefetch_related('genre')
    serializer_class = TitleSerializer
    # permission_classes = [IsAccountAdminOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'delete']
    
    def get_queryset(self):
        queryset = self.queryset
        params_name = {
            'name': 'name__contains',
            'genre': 'genre__slug',
            'category': 'category__slug',
            'year': 'year',
        }

        for param in self.request.query_params:
            param_name = params_name[param]
            queryset = queryset.filter(
                **{param_name: self.request.query_params.get(f'{param}')}
                )
        return queryset

    def validate_data(self, data, param):
        if not data:
            raise ValidationError(f"'{param}': Invalid parameter value!")

    def perform_create(self, serializer):
        model_dict = {
            'category': Categories,
            'genre': Genres,
        }

        result_data = {}
        
        for param in self.request.data:
            if param in model_dict:
                model = model_dict[param]
                data = model.objects.filter(
                    slug=self.request.data.get(f'{param}')
                    )
                self.validate_data(data, param)
                if param == 'category':
                    result_data[param] = data[0]
                else:
                    result_data[param] = data
        serializer.save(**result_data)
    

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenreSerialiser
    # permission_classes = [IsAccountAdminOrReadOnly]
    http_method_names = ['get', 'post', 'delete']
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']

    def perform_create(self, serializer):
        if not self.request.data.get('slug'):
            slug = translit.slugify(self.request.data.get('name'))
            serializer.save(slug=slug)
        serializer.save()


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [IsAccountAdminOrReadOnly]
    http_method_names = ['get', 'post', 'delete']
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']

    def perform_create(self, serializer):
        if not self.request.data.get('slug'):
            slug = translit.slugify(self.request.data.get('name'))
            serializer.save(slug=slug)
        serializer.save()

