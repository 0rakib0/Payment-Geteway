from django.contrib import admin
from django.urls import path, include

# to show media file
from django.conf import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('Shop_app.urls')),
    path('accounts/', include('Auth_app.urls', namespace='default')),
    path('', include('Order_app.urls')),
    path('payment/', include('Payment_app.urls')),
]


urlpatterns +=staticfiles_urlpatterns()
urlpatterns +=static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
