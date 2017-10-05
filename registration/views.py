from custom_user.models import CustomUser
from django.contrib.sites.shortcuts import get_current_site
from django.core import signing
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, reverse, Http404
from django.template import loader
from django.http import JsonResponse
from django.views import generic
from . import forms


class SigningMixIn(object):
    salt = 'registration'

    def check_signing(self, token):
        token_lifetime = 3600 * 72
        try:
            signing.loads(token, salt=self.salt, max_age=token_lifetime)
        except signing.SignatureExpired:
            return False
        except signing.BadSignature:
            raise Http404

    def activate_user(self, token):
        try:
            user = get_object_or_404(CustomUser, pk=signing.loads(token, salt=self.salt))
            user.is_active = True
            user.save()
        except signing.BadSignature:
            raise Http404


class SendEmailMixIn(object):
    def send_token(self):
        context = {
            'site': get_current_site(self.request),
            'username': self.user.username,
            'token': signing.dumps(self.user.pk, salt=self.salt),
        }
        subject = 'Hello'
        body = loader.render_to_string('registration/registration_text.txt', context).strip()
        send_mail(subject, body, 'test-site', [self.user.email], fail_silently=False)


class RegistrationView(SendEmailMixIn, SigningMixIn, generic.FormView):
    template_name = 'registration/registration.html'
    form_class = forms.RegistrationForm
    user = None

    def form_invalid(self, form):
        if self.request.is_ajax:
            return JsonResponse({'errors': form.errors})
        else:
            return super().form_invalid(form)

    def get_success_url(self):
        return reverse('token-sent')

    def form_valid(self, form):
        self.user = CustomUser.objects.create()
        self.user.username = form.cleaned_data.get('username')
        self.user.email = form.cleaned_data.get('email')
        self.user.set_password(form.cleaned_data.get('password_1'))
        self.user.save()
        self.send_token()
        return super().form_valid(form)


class RegistrationConfirm(SigningMixIn, generic.RedirectView):
    token = None

    def get_redirect_url(self, *args, **kwargs):
        if self.check_signing(self.token) is False:
            return reverse('token-expired')
        else:
            return reverse('registration-complete', args=[self.token])

    def dispatch(self, request, *args, **kwargs):
        self.token = kwargs['token']
        return super().dispatch(request, *args, **kwargs)


class RegistrationComplete(SigningMixIn, generic.TemplateView):
    template_name = 'registration/registration_complete.html'

    def dispatch(self, request, *args, **kwargs):
        self.activate_user(kwargs['token'])
        return super().dispatch(request, *args, **kwargs)


class TokenSent(SendEmailMixIn, generic.TemplateView):
    template_name = 'registration/token_sent.html'


class TokenResend(SigningMixIn, SendEmailMixIn, generic.FormView):
    form_class = forms.TokenResendForm
    template_name = 'registration/token_resend.html'
    user = None

    def get_success_url(self):
        return reverse('token-sent')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.user})
        return kwargs

    def form_valid(self, form):
        self.user = form.user
        self.send_token()
        return super().form_valid(form)


class TokenExpired(SigningMixIn, generic.TemplateView):
    template_name = 'registration/token_expired.html'
