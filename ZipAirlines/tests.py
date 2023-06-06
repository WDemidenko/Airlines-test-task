import math

from django.test import TestCase
from rest_framework.test import APIClient
from ZipAirlines.models import Plane
from ZipAirlines.serializers import PlaneDetailSerializer


class PlaneViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.plane = Plane.objects.create(id=1, passengers_amount=100)

    def test_retrieve_all_planes(self):
        response = self.client.get("/api/zipairlines/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), Plane.objects.count())

    def test_retrieve_plane(self):
        response = self.client.get(
            f"/api/zipairlines/{self.plane.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.plane.id)
        self.assertEqual(response.data["passengers_amount"], self.plane.passengers_amount)

    def test_create_plane(self):
        data = {
            "id": 2,
            "passengers_amount": 200
        }
        response = self.client.post("/api/zipairlines/", data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["id"], data["id"])
        self.assertEqual(response.data["passengers_amount"], data["passengers_amount"])

    def test_update_plane(self):
        data = {
            "id": self.plane.id,
            "passengers_amount": 150
        }
        response = self.client.put(f"/api/zipairlines/{self.plane.id}/",
                                   data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], data["id"])
        self.assertEqual(response.data["passengers_amount"], data["passengers_amount"])
        self.plane.refresh_from_db()
        self.assertEqual(self.plane.passengers_amount, data["passengers_amount"])

    def test_delete_plane(self):
        response = self.client.delete(
            f"/api/zipairlines/{self.plane.id}/")
        self.assertEqual(response.status_code, 204)


class PlaneDetailSerializerTest(TestCase):
    def setUp(self):
        self.plane = Plane.objects.create(id=1, passengers_amount=100)
        self.serializer = PlaneDetailSerializer(instance=self.plane)

    def test_get_fuel_consumption_per_min(self):
        fuel_consumption_per_min = self.serializer.get_fuel_consumption_per_min(self.plane)
        expected_fuel_consumption = 0.80 * math.log(self.plane.id) + 0.002 * self.plane.passengers_amount
        self.assertEqual(fuel_consumption_per_min, round(expected_fuel_consumption, 2))

    def test_get_max_flight_duration_in_min(self):
        fuel_consumption_per_min = self.serializer.get_fuel_consumption_per_min(self.plane)
        max_flight_duration = self.plane.fuel_capacity / fuel_consumption_per_min
        expected_max_duration = round(max_flight_duration, 2)

        max_flight_duration_in_min = self.serializer.get_max_flight_duration_in_min(self.plane)
        self.assertEqual(max_flight_duration_in_min, expected_max_duration)
