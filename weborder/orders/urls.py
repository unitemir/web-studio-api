from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import UserProfileListCreateView, UserRegistrationView, UserProfileUpdateView, OrderCreateView, \
    UserOrdersListView, OrderRetrieveView, AttachmentUploadView
from .serializers import UserRegistrationSerializer


class ObtainTokenView(TokenObtainPairView):
    serializer_class = UserRegistrationSerializer


urlpatterns = [
    path('users/', UserProfileListCreateView.as_view(), name='user-list-create'),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('token/', ObtainTokenView.as_view(), name='token_obtain_pair'),
    path('profile/', UserProfileUpdateView.as_view(), name='user-profile-update'),
    path('order/create/', OrderCreateView.as_view(), name='order-create'),
    path('orders/', UserOrdersListView.as_view(), name='user-orders-list'),
    path('order/<str:order_number>/', OrderRetrieveView.as_view(), name='order-retrieve'),
    path('order/attachment/upload/', AttachmentUploadView.as_view(), name='attachment-upload'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
