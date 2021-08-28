from rest_framework.response import Response
from .models import Message
from .serializers import MessageSerializer
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send(request):
    '''
    Sends a message - sender must be the authenticated user to prevent impersonation
    '''
    if request.user.__str__() != request.data['sender'].__str__():
        return Response({'response': 'Authenticated user and sender of the message are mismatched'})

    serializer = MessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response({'response': 'The message is missing some data or invalid'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def read(request):
    '''
    Reading a message - User must be authenticated and pass message_id for the specific message and be either the sender or receiver of the message
    '''
    if 'message_id' not in request.data:
        return Response({"response": "No message with the given id was found"})

    try:
        message = Message.objects.get(Q(message_id=request.data['message_id']),
                                      Q(receiver=request.user))

        message.was_read = True
        message.save()
        request.data['was_read'] = True
        return Response(request.data)
    except:
        return Response({"response": "No message was found"})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete(request):
    '''
    Delete message of the authenticated user - user needs to be authenticated and pass message_id as json variable
    '''

    if 'message_id' not in request.data:
        return Response({"response": "No message with the given id was found"})
    try:
        Message.objects.get(Q(message_id=request.data['message_id']),
                            Q(sender=request.user) | Q(receiver=request.user)).delete()
        return Response({"response": "Message was deleted"})
    except:
        return Response({"response": "No message was found - nothing was deleted"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def show_all_messages(request):
    '''
    Gets all messages of the authenticated user - both read and unread
    '''
    all_messages = Message.objects.all().filter(Q(receiver=request.user))
    serializer = MessageSerializer(all_messages, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def show_all_unread_messages(request):
    '''
    Get all unread messages of the authenticated user
    '''
    all_messages = Message.objects.all().filter(
        Q(receiver=request.user), was_read=False)
    serializer = MessageSerializer(all_messages, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
def delete_all_messages(request):
    Message.objects.all().delete()
    return Response({"response": "All messages were deleted from all users"})
