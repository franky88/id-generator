from django.urls import path, include
# from rest_framework import routers
from . import views

# router = routers.DefaultRouter()
# router.register(r'idinfo', views.IdInfoViewSet)

app_name = "idgen"
urlpatterns = [
    # path('', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', views.home, name="home"),
    path('add-id', views.add_id, name="add"),
    path('details/<pk>', views.update_id, name="details"),
    path('delete/<pk>', views.delete, name="delete"),
    path('preview-id/<pk>', views.view_id, name="view")
]
