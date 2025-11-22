"""Views for the Recipe API.

This module contains viewsets used by the recipe API. The implementation
is unchanged from the original logic — only formatting, docstrings and
comments were improved to follow PEP 8 and make the code easier to
maintain and read.
"""

# Third-party imports
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiTypes,
    extend_schema,
    extend_schema_view,
)
from rest_framework import mixins, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Local imports
from .models import Ingredient, Recipe, Tag
from .serializers import (
    IngredientSerializer,
    RecipeDetailsSerializer,
    RecipeImageSerializer,
    RecipeSerializer,
    TagSerialization,
)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                "tags",
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
                description="Comma-separated list of tag IDs to filter by.",
            ),
            OpenApiParameter(
                "ingredient",
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
                description="Comma-separated list of ingredient IDs to filter by.",
            ),
        ]
    )
)
class RecipeViewset(viewsets.ModelViewSet):
    """ViewSet for managing recipes.

    The viewset supports listing, retrieving, creating, updating and
    deleting recipes. It also exposes a custom action to upload images.
    Filtering by comma-separated tag and ingredient ID lists is supported
    through query parameters.
    """

    serializer_class = RecipeDetailsSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def _params_to_ints(self, qs):
        """Convert a comma-separated string of IDs to a list of ints.

        Args:
            qs (str): Comma-separated IDs, e.g. "1,2,3".

        Returns:
            list[int]: Converted integer ID list.
        """
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        """Return recipes for the authenticated user, optionally filtered.

        Supports the following query parameters:
        - tags: comma-separated tag IDs
        - ingredient: comma-separated ingredient IDs
        """
        tags = self.request.query_params.get("tags")
        ingredient = self.request.query_params.get("ingredient")
        queryset = self.queryset

        if tags:
            tags_id = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tags_id)

        if ingredient:
            ingredient_id = self._params_to_ints(ingredient)
            queryset = queryset.filter(ingredient__id__in=ingredient_id)

        return (
            queryset.filter(user=self.request.user)
            .order_by("-id")
            .distinct()
        )

    def get_serializer_class(self):
        """Return appropriate serializer class based on action."""
        if self.action == "list":
            return RecipeSerializer

        if self.action == "upload_image":
            return RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Save a new recipe instance assigning the current user."""
        serializer.save(user=self.request.user)

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
        parser_classes=[MultiPartParser, FormParser],
    )
    def upload_image(self, request, pk=None):
        """Custom action to upload an image for a recipe.

        The action expects multipart/form-data and returns the serialized
        recipe on success or validation errors on failure.
        """
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                "assigned_only",
                OpenApiTypes.INT,
                enum=[0, 1],
                description="Filter by items assigned to recipes (0 or 1).",
            )
        ]
    )
)
class BaseRecipeAttrViewSet(
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Base viewset for recipe attributes like tags and ingredients.

    Provides list, update and delete operations and restricts results to
    objects owned by the authenticated user. Subclasses should define
    queryset and serializer_class attributes.
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return queryset filtered by the authenticated user.

        If the `assigned_only` query parameter equals 1, only return items
        that are assigned to at least one recipe.
        """
        assigned_only = bool(int(self.request.query_params.get("assigned_only", 0)))
        queryset = self.queryset

        if assigned_only:
            queryset = queryset.filter(recipe__isnull=False)

        return queryset.filter(user=self.request.user).order_by("-name").distinct()


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database."""

    serializer_class = TagSerialization
    queryset = Tag.objects.all()


class IngredientViewset(BaseRecipeAttrViewSet):
    """Manage ingredients in the database."""

    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
