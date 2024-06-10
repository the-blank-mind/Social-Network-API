from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import FriendRequest
from .serializers import UserSerializer, FriendRequestSerializer
from datetime import timezone

User = get_user_model()

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login(request):
    email = request.data.get('email').lower()
    password = request.data.get('password')
    user = User.objects.filter(email=email).first()

    if user and user.check_password(password):
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def search_users(request):
    query = request.query_params.get('q', '')
    users = User.objects.filter(Q(email__iexact=query) | Q(username__icontains=query))
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def respond_friend_request(request, pk):
    user = request.user
    try:
        friend_request = FriendRequest.objects.get(id=pk, receiver=user)
        status = request.data.get('status')
        if status == 'accepted':
            friend_request.status = 'accepted'
            friend_request.save()
            
        elif status == 'rejected':
            friend_request.status = 'rejected'
            friend_request.save()
        else:
            return Response({"detail": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": f"Friend request {status}"})
    except FriendRequest.DoesNotExist:
        return Response({"detail": "Friend request not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])    
def send_friend_request(request):
    sender = request.user
    receiver_id = request.data.get('receiver_id')
    if not receiver_id:
        return Response({"detail": "Receiver ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        receiver = User.objects.get(id=receiver_id)
        one_minute_ago = timezone.now() - timezone.timedelta(minutes=1)
        recent_requests_count = FriendRequest.objects.filter(
            sender=sender, 
            created_at__gte=one_minute_ago
        ).count()

        if recent_requests_count >= 3:
            return Response({"detail": "You have exceeded the limit of friend requests per minute"}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        if FriendRequest.objects.filter(sender=sender, receiver=receiver).exists():
            return Response({"detail": "Friend request already sent"}, status=status.HTTP_400_BAD_REQUEST)

        friend_request = FriendRequest(sender=sender, receiver=receiver)
        friend_request.save()
        FriendRequest.objects.create(sender=sender, receiver=receiver)
        return Response({"detail": "Friend request sent"}, status=status.HTTP_201_CREATED)
    except User.DoesNotExist:
        return Response({"detail": "Receiver not found"}, status=status.HTTP_404_NOT_FOUND)    
 
    
    
    
    
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_friends(request):
    user = request.user
    friends = User.objects.filter(
        Q(sent_requests__receiver=user, sent_requests__status='accepted') |
        Q(received_requests__sender=user, received_requests__status='accepted')
    ).distinct()
    serializer = UserSerializer(friends, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def pending_requests(request):
    user=request.user
    pending_requests = request.user.received_requests.filter(status='pending')
    serializer = FriendRequestSerializer(pending_requests, many=True)
    return Response(serializer.data)
