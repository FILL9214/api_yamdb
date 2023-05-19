from rest_framework import serializers
from reviews.models import (
    Category,
    Genre,
    Title,
    Comment,
    Review,
    User
)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(
        read_only=True
    )
    genre = GenreSerializer(
        many=True,
        read_only=True,
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = ('id',
                  'name',
                  'year',
                  'description',
                  'category',
                  'genre',
                  'rating')
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления и
    частичного изменения информации о произведении.
    """
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
        many=False,
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'description',
            'year',
            'genre',
            'category',
        )


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

    # по урокам с котиками и тырнету вроде оно
    def create(self, validated_data):
        user = User.objects.get_or_create(**validated_data)
        return user


class TokenSerializer(serializers.Serializer):
    """Сериализатор получение токена."""
    username = serializers.CharField(
        max_length=150
    )
    confirmation_code = serializers.CharField()
