from rest_framework import serializers
from reviews.models import (
    Category,
    Genre,
    Title,
    GenreTitle,
    Comment,
    Review,
    User
)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, required=False)

    class Meta:
        fields = ('id', 'year', 'description', 'category', 'genres')
        model = Title

    def create(self, validated_data):
        genres = validated_data.pop('genres')
        title = Title.objects.create(**validated_data)
        for genre in genres:
            current_genre, status = Genre.objects.get_or_create(**genre)
            GenreTitle.objects.create(genre=current_genre, title=title)
        return title


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


class AdminModerSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя с ролью 'moderator', 'admin'."""
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class SimpleUserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя с ролью 'user'."""
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор получение кода подтверждения."""
    class Meta:
        model = User
        fields = ('email', 'username')


class TokenSerializer(serializers.Serializer):
    """Сериализатор получение токена."""
    username = serializers.CharField(
        max_length=150
    )
    confirmation_code = serializers.CharField()
