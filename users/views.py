from django.shortcuts import render
# views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Match
from django.contrib.auth.models import User
from .serializers import MatchSerializer
from django.shortcuts import get_object_or_404

# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_match_request(request):
    to_user_id = request.data.get('to_user_id')
    to_user = get_object_or_404(User, id=to_user_id)

    match, created = Match.objects.get_or_create(
        from_user=request.user,
        to_user=to_user,
        defaults={'status': 'pending'}
    )
    if not created:
        return Response({'message': 'Request already exists'}, status=400)

    serializer = MatchSerializer(match)
    return Response(serializer.data, status=201)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def respond_to_match(request, match_id):
    match = get_object_or_404(Match, id=match_id, to_user=request.user)

    response = request.data.get('response')  # "confirm" or "reject"
    if response == 'confirm':
        match.status = 'confirmed'
    elif response == 'reject':
        match.status = 'rejected'
    else:
        return Response({'error': 'Invalid response'}, status=400)

    match.save()
    serializer = MatchSerializer(match)
    return Response(serializer.data)


