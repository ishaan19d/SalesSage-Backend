from django.urls import path
from .views import ItemsView, SalesUploadView, SalesListView

urlpatterns = [
    path('items/',ItemsView.as_view(), name='items'),
    path('upload-sales/',SalesUploadView.as_view(), name='upload-sales'),
    path('view-sales/',SalesListView.as_view(), name='sales'),
]