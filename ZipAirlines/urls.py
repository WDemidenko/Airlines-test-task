from rest_framework.routers import DefaultRouter

from ZipAirlines.views import PlaneViewSet

router = DefaultRouter()
router.register("", PlaneViewSet)

urlpatterns = router.urls

app_name = "zipairlines"
