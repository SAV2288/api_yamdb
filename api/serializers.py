from rest_framework import serializers


from .models import Review, Comment, Rate, Genres, Titles, Categories


class ScoreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['score']
        model = Rate


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    score = ScoreSerializer()

    class Meta:
        fields = ['id', 'text', 'author', 'score', 'pub_date']
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'author', 'text', 'created')
        model = Comment


class GenreSerialiser(serializers.ModelSerializer):
    slug = serializers.SlugField(required=False)
    class Meta:
        fields = ('name', 'slug')
        model = Genres


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(required=False)
    class Meta:
        fields = ('name', 'slug')
        model = Categories


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerialiser(many=True, required=False, read_only=True)
    category = CategorySerializer(required=False, read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Titles

