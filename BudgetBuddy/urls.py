from django.contrib import admin

from django.urls import path, include

from django.conf import settings

from django.conf.urls.static import static

urlpatterns = [

path('admin/', admin.site.urls),

path('', include('apps.accounts.urls')),

path("income/", include("apps.income.urls")),

path("expense/", include("apps.expense.urls")),

path("budgets/", include("apps.budgets.urls")),

path("reports/", include("apps.reports.urls")),

path("notifications/",include("apps.notifications.urls")),
     
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
