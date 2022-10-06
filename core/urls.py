from rest_framework.routers import DefaultRouter
from core import viewsets

router = DefaultRouter()
router.register('state', viewsets.StateViewSet)
router.register('marital_status', viewsets.MaritalStatusViewSet)
router.register('employee', viewsets.EmployeeViewSet)
router.register('branch', viewsets.BranchViewSet)
router.register('department', viewsets.DepartmentViewSet)
router.register('sale', viewsets.SaleViewSet)
router.register('sale_item', viewsets.SaleItemViewSet)

urlpatterns = router.urls
