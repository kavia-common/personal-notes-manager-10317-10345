from django.contrib.auth import authenticate, login, logout
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Note
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    NoteSerializer,
)
from .permissions import IsOwnerOrReadOnly


# PUBLIC_INTERFACE
@swagger_auto_schema(
    method="get",
    operation_id="health_check",
    operation_summary="Health check",
    operation_description="Returns a simple message indicating the server is running.",
    responses={200: openapi.Response("OK", schema=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
        "message": openapi.Schema(type=openapi.TYPE_STRING)
    }))},
    tags=["System"],
)
@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def health(request):
    """Health endpoint."""
    return Response({"message": "Server is up!"}, status=200)


# PUBLIC_INTERFACE
@swagger_auto_schema(
    method="post",
    operation_id="auth_register",
    operation_summary="Register user",
    operation_description="Create a new user account.",
    request_body=UserRegistrationSerializer,
    responses={201: openapi.Response("Created")},
    tags=["Auth"],
)
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def register(request):
    """Register a new user with username, email, and password."""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"detail": "User registered successfully."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# PUBLIC_INTERFACE
@swagger_auto_schema(
    method="post",
    operation_id="auth_login",
    operation_summary="Login user",
    operation_description="Authenticate a user using username and password. Uses session authentication.",
    request_body=UserLoginSerializer,
    responses={
        200: openapi.Response("OK", schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"detail": openapi.Schema(type=openapi.TYPE_STRING)}
        )),
        400: "Bad Request",
        401: "Unauthorized",
    },
    tags=["Auth"],
)
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """Login with username and password; creates a session cookie."""
    serializer = UserLoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    username = serializer.validated_data["username"]
    password = serializer.validated_data["password"]
    user = authenticate(request, username=username, password=password)
    if user is None:
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
    login(request, user)
    return Response({"detail": "Logged in successfully."}, status=status.HTTP_200_OK)


# PUBLIC_INTERFACE
@swagger_auto_schema(
    method="post",
    operation_id="auth_logout",
    operation_summary="Logout user",
    operation_description="Logs out the current authenticated user.",
    responses={200: "OK"},
    tags=["Auth"],
)
@api_view(["POST"])
def logout_view(request):
    """Logout the current user by clearing the session."""
    logout(request)
    return Response({"detail": "Logged out successfully."}, status=status.HTTP_200_OK)


class IsAuthenticatedAndOwner(permissions.IsAuthenticated, IsOwnerOrReadOnly):
    """Combined permission for authenticated users and ownership checks."""
    pass


# PUBLIC_INTERFACE
class NoteViewSet(viewsets.ModelViewSet):
    """
    ViewSet providing CRUD operations for notes.
    Only authenticated users can access.
    Notes are always scoped to the authenticated user's ownership.
    """
    serializer_class = NoteSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticatedAndOwner,)

    def get_queryset(self):
        """Return notes owned by the current user."""
        return Note.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """Assign the authenticated user as the owner on create."""
        serializer.save(owner=self.request.user)

    # Document list and create operations
    @swagger_auto_schema(
        operation_id="notes_list",
        operation_summary="List notes",
        operation_description="List notes owned by the authenticated user.",
        tags=["Notes"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="notes_create",
        operation_summary="Create a note",
        operation_description="Create a new note owned by the authenticated user.",
        tags=["Notes"],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="notes_retrieve",
        operation_summary="Retrieve a note",
        operation_description="Retrieve a note by ID, only if owned by the authenticated user.",
        tags=["Notes"],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="notes_update",
        operation_summary="Update a note",
        operation_description="Update a note by ID, only if owned by the authenticated user.",
        tags=["Notes"],
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="notes_partial_update",
        operation_summary="Partially update a note",
        operation_description="Partially update a note by ID, only if owned by the authenticated user.",
        tags=["Notes"],
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="notes_destroy",
        operation_summary="Delete a note",
        operation_description="Delete a note by ID, only if owned by the authenticated user.",
        tags=["Notes"],
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
