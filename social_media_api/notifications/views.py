from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer, NotificationUpdateSerializer, NotificationCountSerializer
from .pagination import NotificationPagination


# Create your views here.
@login_required
def notifications_view(request):
    return render(request, 'notifications/notifications.html')

class NotificationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    pagination_class = NotificationPagination

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

    def list(self, request):
        queryset = self.get_queryset()
        read_status = self.request.query_params.get('read', None)
        if read_status is not None:
            if read_status.lower() == 'true':
                queryset = queryset.filter(read=True)
            elif read_status.lower() == 'false':
                queryset = queryset.filter(read=False)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.mark_as_read()
        return Response({'message': 'Notification marked as read'})

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        updated_count = self.get_queryset().filter(read=False).update(read=True)
        return Response({'message': f'Marked {updated_count} notifications as read'})

    @action(detail=False, methods=['get'])
    def count(self, request):
        total_count = self.get_queryset().count()
        unread_count = self.get_queryset().filter(read=False).count()

        serializer = NotificationCountSerializer({
            'unread_count': unread_count,
            'total_count': total_count
        })
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def unread(self, request):
        unread_notifications = self.get_queryset().filter(read=False)
        
        page = self.paginate_queryset(unread_notifications)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(unread_notifications, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def notification_stats(request):
    notifications = Notification.objects.filter(recipient=request.user)

    stats = {
        'total': notifications.count(),
        'unread': notifications.filter(read=False).count(),
        'read': notifications.filter(read=True).count(),
        'types': {
            'follow': notifications.filter(verb='follow').count(),
            'like_post': notifications.filter(verb='like_post').count(),
            'like_comment': notifications.filter(verb='like_comment').count(),
            'comment': notifications.filter(verb='comment').count(),
            'mention': notifications.filter(verb='mention').count(),
        }
    }
    return Response(stats)
