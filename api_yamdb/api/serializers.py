from rest_framework import serializers
from reviews.models import Comment, Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    review = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    class Meta:
        fields = '__all__'
        model = Review

    def create(self, validated_data):
        if Review.objects.filter(
            author=self.context['request'].user,
            title=validated_data.get('title')
        ).exists():
            raise serializers.ValidationError(
                'Нельзя оставить больше одного обзора.')
        review = Review.objects.create(**validated_data,)
        return review
