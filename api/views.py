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
    serializer_class = TitleSerializer
    # permission_classes = [IsAccountAdminOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def queryset_filter(self, queryset):
        params_name = {
            'name': 'name__contains',
            'genre': 'genre__slug',
            'category': 'category__slug',
            'year': 'year',
        }

        for param in self.request.query_params:
            if param in params_name:
                param_name = params_name[param]
                queryset = queryset.filter(
                    **{param_name: self.request.query_params.get(f'{param}')}
                    )
    
    def get_queryset(self):
        queryset = Titles.objects.select_related('category').all().prefetch_related('genre')
        
        if self.request.query_params:
            queryset = queryset_filter(queryset)

        return queryset

    def validate_data(self, data, param):
        if not data:
            raise ValidationError(f"'{param}': Invalid parameter value!")

    def get_related_parameters(self):
        result_data = {}
        model_dict = {
            'category': Categories,
            'genre': Genres,
        }
        
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
        return result_data

    def perform_create(self, serializer):
        result_data = self.get_related_parameters()
        serializer.save(**result_data)

    def perform_update(self, serializer):
        result_data = self.get_related_parameters()
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