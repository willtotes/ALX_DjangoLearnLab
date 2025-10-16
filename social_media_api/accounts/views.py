from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from .models import CustomUser
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, UserUpdateSerializer, FollowActionSerializer, UserDetailSerializer, UserFollowSerializer
from notifications.models import Notification

# Create your views here.
def register_view(request):
    if request.user.is_authenticated:
        return redirect('feed')
    return render(request, 'accounts/register.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('feed')
    return render(request, 'accounts/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserRegistrationSerializer(data = request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user = user)
        return Response({
            'token': token.key,
            'user': UserProfileSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    serializer = UserLoginSerializer(data = request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user = user)
        return Response({
            'token': token.key,
            'user': UserProfileSerializer(user).data
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    if request.method == 'GET':
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserUpdateSerializer(request.user, data = request.data, partial= True)
        if serializer.is_valid():
            serializer.save()
            return Response(UserProfileSerializer(request.user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    try:
        request.user.auth_token.delete()
        return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request):
    serializer = FollowActionSerializer(data = request.data, context = {'request': request})
    if serializer.is_valid():
        user_to_follow = get_object_or_404(CustomUser, id = serializer.validated_data['user_id'])

        if request.user.follow(user_to_follow):
            Notification.create_notification(
                recipient=user_to_follow,
                actor=request.user,
                verb='follow'
            )
            return Response({
                'message': f'You are now following {user_to_follow.username}',
                'following': True,
                'followers_count': user_to_follow.followers_count,
                'following_count': request.user.following_count
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'You are already following this user or cannot follow yourself'
            }, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request):
    serializer = FollowActionSerializer(data = request.data, context = {'request': request})

    if serializer.is_valid():
        user_to_unfollow = get_object_or_404(CustomUser, id = serializer.validated_data['user_id'])
        if request.user.unfollow(user_to_unfollow):
            return Response({
                'message': f'You have unfollowed {user_to_unfollow.username}',
                'following': False,
                'followers_count': user_to_unfollow.followers_count,
                'following_count': request.user.following_count
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'You are not following this user'
            }, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_followers(request):
    followers = request.user.followers.all()
    serializer = UserFollowSerializer(followers, many = True, context = {'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_following(request):
    following = request.user.following.all()
    serializer = UserFollowSerializer(following, many = True, context = {'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_detail(request, user_id):
    user = get_object_or_404(CustomUser, id = user_id)
    serializer = UserDetailSerializer(user, context = {'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_search(request):
    query = request.query_params.get('q', '')
    if not query:
        return Response({'error': 'Query parameters "q" is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    users = CustomUser.objects.filter(username__icontains=query)[:10]
    serializer = UserFollowSerializer(users, many = True, context = {'request': request})
    return Response(serializer.data)