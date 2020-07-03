from django.db.models import Prefetch

from rest_framework import viewsets
from rest_framework import filters

from api.models import Titles
from api.models import Genres
from api.models import Categories
from api.serializers import GenreSerialiser
from api.serializers import CategorySerializer
from api.serializers import TitleSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.select_related('category').all().prefetch_related('genre')
    serializer_class = TitleSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    
    def get_queryset(self):
        queryset = self.queryset
        key = {
            'name': 'name__contains',
            'genre': 'genre__slug',
            'category': 'category__slug',
            'year': 'year',
        }

        for param in self.request.query_params:
            param_key = key[param]
            queryset = queryset.filter(
                **{param_key: self.request.query_params.get(f'{param}')}
                )
        return queryset

    # def perform_create(self, serializer):

    #     serializer.save()
    

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenreSerialiser
    http_method_names = ['get', 'post', 'delete']
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ['get', 'post', 'delete']
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
