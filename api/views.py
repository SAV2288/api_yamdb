from django.db.models import Prefetch
from django.template.defaultfilters import slugify

from rest_framework import viewsets
from rest_framework import filters
from rest_framework.exceptions import ValidationError

from pytils import translit

from api.models import Titles
from api.models import Genres
from api.models import Categories
from api.serializers import GenreSerialiser
from api.serializers import CategorySerializer
from api.serializers import TitleSerializer


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