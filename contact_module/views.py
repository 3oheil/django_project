from django.views.generic import CreateView, ListView

from site_setting.models import SiteSetting, SiteBanner
from .forms import ContactUsForm
from .models import ContactUs, CreateProfile


# Create your views here.

class ContactUsView(CreateView):
    template_name = 'contact_module/contact_us_page.html'
    model = ContactUs
    form_class = ContactUsForm
    success_url = '/contact-us/'
    context_object_name = 'form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setting: SiteSetting = SiteSetting.objects.filter(is_mean_site=True).first()
        context['site_setting'] = setting
        context['banners'] = SiteBanner.objects.filter(is_active=True,
                                                       position__iexact=SiteBanner.PositionBannerChoices.contact_us)
        return context


class CreateProfileView(CreateView):
    template_name = 'contact_module/create_profile_page.html'
    model = CreateProfile
    fields = '__all__'
    success_url = '/contact-us/create-profile'


class ProfileListView(ListView):
    template_name = 'contact_module/profile_list_page.html'
    model = CreateProfile
    context_object_name = 'profiles'
