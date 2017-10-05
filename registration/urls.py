from django.conf.urls import url
from . import views




urlpatterns = [
    url(regex='^registration/$',
        view=views.RegistrationView.as_view(),
        name='registration',),

    url(regex='^token_sent/$',
        view=views.TokenSent.as_view(),
        name='token-sent'),

    url(regex='^token_resend/$',
        view=views.TokenResend.as_view(),
        name='token-resend'),

    url(regex='^registration_confirm/(?P<token>[\w:-]+)/$',
        view=views.RegistrationConfirm.as_view(),
        name='registration-confirm'),

    url(regex='^registration_complete/(?P<token>[\w:-]+)/$',
        view=views.RegistrationComplete.as_view(),
        name='registration-complete')
]
