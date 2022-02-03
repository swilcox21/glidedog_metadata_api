from unicodedata import name
from django.urls import include, path
from rest_framework import routers
from .views import UserViewSet,TableViewSet,DatasetView,TableView,ColumnView,TableTruncateView,DatasetTruncateView
router = routers.DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'table/new', TableViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(router.urls)),
    path('dataset', DatasetView.as_view(), name='dataset'),
    path('dataset/<int:dataset_id>', DatasetView.as_view(), name='dataset'),
    path('dataset/<int:dataset_id>/truncate', DatasetTruncateView.as_view(), name='dataset'),
    path('table', TableView.as_view(), name='table'),
    path('table/<int:table_id>', TableView.as_view(), name='table'),
    path('table/<int:table_id>/truncate', TableTruncateView.as_view(), name='table'),
    path('column', ColumnView.as_view(), name='column'),
    path('column/<int:column_id>', ColumnView.as_view(), name='column'),
]