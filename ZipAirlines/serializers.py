import math

from rest_framework import serializers

from ZipAirlines.models import Plane


class PlaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plane
        fields = ("id", "passengers_amount")


class PlaneDetailSerializer(PlaneSerializer):

    fuel_consumption_per_min = serializers.SerializerMethodField()
    max_flight_duration_in_min = serializers.SerializerMethodField()

    class Meta:
        model = Plane
        fields = ("id", "passengers_amount", "fuel_consumption_per_min", "max_flight_duration_in_min")

    def get_fuel_consumption_per_min(self, obj):
        fuel_consumption_id = math.log(obj.id) * 0.80
        fuel_consumption_passengers = obj.passengers_amount * 0.002
        fuel_consumption_per_min = fuel_consumption_id + fuel_consumption_passengers
        return round(fuel_consumption_per_min, 2)

    def get_max_flight_duration_in_min(self, obj):
        fuel_consumption_per_min = self.get_fuel_consumption_per_min(obj)
        max_flight_duration = obj.fuel_capacity / fuel_consumption_per_min
        return round(max_flight_duration, 2)
