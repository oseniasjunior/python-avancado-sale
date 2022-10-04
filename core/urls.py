from rest_framework.routers import DefaultRouter
from core import viewsets

router = DefaultRouter()
router.register('state', viewsets.StateViewSet)
router.register('employee', viewsets.EmployeeViewSet)
router.register('branch', viewsets.BranchViewSet)
router.register('department', viewsets.DepartmentViewSet)

urlpatterns = router.urls
