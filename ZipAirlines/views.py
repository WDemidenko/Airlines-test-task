from rest_framework import mixins, viewsets

from ZipAirlines.models import Plane
from ZipAirlines.serializers import PlaneSerializer, PlaneDetailSerializer


class PlaneViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Plane.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PlaneDetailSerializer
        return PlaneSerializer
