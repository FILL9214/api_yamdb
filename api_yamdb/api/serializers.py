from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import (
    Category,
    Genre,
    Title,
    Comment,
    Review,
    User
)

from reviews.validators import validate_username


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
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        many=False,
    )
    score = serializers.IntegerField(max_value=10, min_value=1)

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise serializers.ValidationError(
                'Может существовать только один отзыв.')
        return data

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        read_only = ('id',)
        model = Review


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


class SignUpSerializer(serializers.Serializer):
    """Сериализатор получение кода подтверждения."""
    email = serializers.EmailField(
        max_length=254,
        required=True
    )
    username = serializers.RegexField(
        max_length=150,
        regex=r'^[\w.@+-]+\Z',
        required=True
    )

    def validate_username(self, value):
        return validate_username(value)

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        data = super().validate(data)
        email = data.get('email')
        username = data.get('username')
        if (
            not User.objects.filter(email=email, username=username)
            and User.objects.filter(email=email)
        ):
            raise serializers.ValidationError('Этот адрес почты занят')
        if (
            not User.objects.filter(email=email, username=username)
            and User.objects.filter(username=username)
        ):
            raise serializers.ValidationError('Этот имя уже занято')
        return data


class TokenSerializer(serializers.Serializer):
    """Сериализатор получение токена."""
    username = serializers.CharField(
        max_length=150
    )
    confirmation_code = serializers.CharField()
