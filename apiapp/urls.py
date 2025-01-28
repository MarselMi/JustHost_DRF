from rest_framework import routers
from .views import VPSViewSet


router = routers.DefaultRouter()
router.register(r'vps', VPSViewSet)
