from rest_framework import serializers

from .models import Review, Comment, Rate


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
