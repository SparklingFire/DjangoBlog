from django.conf.urls import url
from . import views




urlpatterns = [
    url(regex='^password_recovery/$',
        view=views.PasswordRecoveryView.as_view(),
        name='password-recovery'),

    url(regex='^password_change/$',
        view=views.PasswordChangeView.as_view(),
        name='password-change'),

    url(regex='^password_recovery/(?P<token>[\w:-]+)/$',
        view=views.PasswordReset.as_view(),
        name='password-reset'),

    url(regex='^password_recovery/email_sent/$',
        view=views.PasswordRecoverySent.as_view(),
        name='password-recovery-sent'),
]
