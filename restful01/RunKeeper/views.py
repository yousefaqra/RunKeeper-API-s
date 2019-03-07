from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from . models import Session
from . serializers import SessionSerializer
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import filters
from django_filters import AllValuesFilter, DateTimeFilter, NumberFilter
from rest_framework.permissions import IsAuthenticated
from . import custompermission
from rest_framework.throttling import ScopedRateThrottle
from django.db.models import Sum
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from django.contrib.auth import login, logout
from rest_framework.authtoken.models import Token
from rest_framework import status

# Create your views here.


class SessionFilter(filters.FilterSet):
    min_distance_in_miles = NumberFilter(
        'distance_in_miles', lookup_expr='gte')
    max_distance_in_miles = NumberFilter(
        'distance_in_miles', lookup_expr='lte')

    class Meta:
        model = Session
        fields = ('distance_in_miles',
                  'min_distance_in_miles',
                  'max_distance_in_miles',)


# uri:  /sessions/

class SessionList(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    throttle_scope = 'session'
    throttle_classes = (ScopedRateThrottle,)

    name = 'session-list'

    filter_class = SessionFilter
    serializer_class = SessionSerializer
    ordering_fields = (
        'distance_in_miles',
        'speed'
    )

    def get_queryset(self):
        return Session.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# uri:  /sessions/pk
class SessionSpecificSpeed(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated,
                          custompermission.IsCurrentUserOwner]
    throttle_scope = 'session'
    throttle_classes = (ScopedRateThrottle,)

    name = 'Specific-Speed'

    def get(self, request, pk, format=None):
        queryset = Session.objects.get(id=pk)
        self.check_object_permissions(self.request, queryset)
        dist = queryset.distance_in_miles
        time = queryset.length_of_run
        speed = dist / time

        return Response({
            'Session Speed': speed})


# uri:  /sessions/totaldistance
class TotalDistance(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    throttle_scope = 'session'

    serializer_class = SessionSerializer
    name = 'total-distance'

    authentication_classes = (
        TokenAuthentication,
    )

    def get(self, request, *args, **kwargs):

        queryset = Session.objects.filter(owner=self.request.user)

        sum_dist = queryset.aggregate(Sum('distance_in_miles'))
        total_dist = sum_dist['distance_in_miles__sum']

        return Response({
            'total distance run over all running sessions': total_dist})


# uri: /sessions/averagespeed
class AverageSpeed(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    throttle_scope = 'session'
    throttle_classes = (ScopedRateThrottle,)
    name = 'average-speed'

    def get(self, request, *args, **kwargs):

        queryset = Session.objects.filter(owner=self.request.user)

        dist = queryset.aggregate(Sum('distance_in_miles'))
        time = queryset.aggregate(Sum('length_of_run'))
        avg = dist['distance_in_miles__sum'] / time['length_of_run__sum']

        return Response({
            'Average Speeds': avg})


# uri: /sessions/login
class LoginView(generics.GenericAPIView):
    name = "login"

    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        token = Token.objects.get(user=self.request.user)
        token, created = Token.objects.get_or_create(user=self.request.user)
        return Response({
            "Token": token.key},
            status=status.HTTP_200_OK
        )


# uri: /sessions/logout
class LogoutView(generics.GenericAPIView):
    name = 'logout'
    authentication_classes = (
        TokenAuthentication,
    )

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


# uri: "localhost:8000/"
class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({
            'sessions': reverse(SessionList.name, request=request),
            'total distance run over all running sessions': reverse(TotalDistance.name, request=request),
            'average speed run over all running sessions': reverse(AverageSpeed.name, request=request),
        })
