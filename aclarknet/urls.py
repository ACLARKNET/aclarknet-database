"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from .database import views
from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'clients', views.ClientViewSet)
router.register(r'services', views.ServiceViewSet)
router.register(r'testimonials', views.TestimonialViewSet)
router.register(r'profiles', views.ProfileViewSet)

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    # API
    url(r'^api/', include(router.urls)),
    # Client
    url(r'^client/(?P<pk>\d+)$', views.client, name='client'),
    url(r'^client/(?P<pk>\d+)/edit$', views.client_edit, name='client_edit'),
    url(r'^client/add$', views.client_edit, name='client_edit'),
    url(r'^client$', views.client_index, name='client_index'),
    # Contact
    url(r'^contact/(?P<pk>\d+)$', views.contact, name='contact'),
    url(r'^contact/(?P<pk>\d+)/edit$', views.contact_edit,
        name='contact_edit'),
    url(r'^contact/add$', views.contact_edit, name='contact_edit'),
    url(r'^contact$', views.contact_index, name='contact_index'),
    url(r'^contact/(?P<pk>\d+)/mail$', views.contact_mail,
        name='contact_mail'),
    url(r'^contact/(?P<pk>\d+)/unsubscribe$',
        views.contact_unsubscribe,
        name='contact_unsubscribe'),
    # Contract
    url(r'^contract/(?P<pk>\d+)$', views.contract, name='contract'),
    url(r'^contract/(?P<pk>\d+)/edit$',
        views.contract_edit,
        name='contract_edit'),
    url(r'^contract/add$', views.contract_edit, name='contract_edit'),
    url(r'^contract$', views.contract_index, name='contract_index'),
    # Estimate
    url(r'^estimate/(?P<pk>\d+)$', views.estimate, name='estimate'),
    url(r'^estimate/(?P<pk>\d+)/edit$',
        views.estimate_edit,
        name='estimate_edit'),
    url(r'^estimate/(?P<pk>\d+)/mail$',
        views.estimate_mail,
        name='estimate_mail'),
    url(r'^estimate/add$', views.estimate_edit, name='estimate_edit'),
    url(r'^estimate$', views.estimate_index, name='estimate_index'),
    # Invoice
    url(r'^invoice/(?P<pk>\d+)$', views.invoice, name='invoice'),
    url(r'^invoice/(?P<pk>\d+)/edit$', views.invoice_edit,
        name='invoice_edit'),
    url(r'^invoice/add$', views.invoice_edit, name='invoice_edit'),
    url(r'^invoice$', views.invoice_index, name='invoice_index'),
    # Login
    url(r'^login$', views.login, name='login'),
    # Logs
    url(r'^log$', views.log_index, name='log_index'),
    # Newsletter
    url(r'^newsletter/(?P<pk>\d+)$', views.newsletter, name='newsletter'),
    url(r'^newsletter/(?P<pk>\d+)/edit$',
        views.newsletter_edit,
        name='newsletter_edit'),
    url(r'^newsletter/(?P<pk>\d+)/send$',
        views.newsletter_send,
        name='newsletter_send'),
    url(r'^newsletter/add$', views.newsletter_edit, name='newsletter_edit'),
    url(r'^newsletter$', views.newsletter_index, name='newsletter_index'),
    # Note
    url(r'^note/(?P<pk>\d+)$', views.note, name='note'),
    url(r'^note/(?P<pk>\d+)/edit$', views.note_edit, name='note_edit'),
    url(r'^note/add$', views.note_edit, name='note_edit'),
    url(r'^note$', views.note_index, name='note_index'),
    # Project
    url(r'^project/(?P<pk>\d+)$', views.project, name='project'),
    url(r'^project/(?P<pk>\d+)/edit$', views.project_edit,
        name='project_edit'),
    url(r'^project/add$', views.project_edit, name='project_edit'),
    url(r'^project$', views.project_index, name='project_index'),
    # Proposal
    url(r'^proposal/(?P<pk>\d+)$', views.proposal, name='proposal'),
    url(r'^proposal/(?P<pk>\d+)/edit$',
        views.proposal_edit,
        name='proposal_edit'),
    url(r'^proposal/add$', views.proposal_edit, name='proposal_edit'),
    url(r'^proposal$', views.proposal_index, name='proposal_index'),
    # Report
    url(r'^report/(?P<pk>\d+)$', views.report, name='report'),
    url(r'^report$', views.report_index, name='report_index'),
    url(r'^report/add$', views.report_edit, name='report_edit'),
    url(r'^report/(?P<pk>\d+)/edit$', views.report_edit, name='report_edit'),
    url(r'^report_plot$', views.report_plot, name='report_plot'),
    # Settings -> System
    url(r'^settings/system/edit$', views.settings_edit, name='settings_edit'),
    url(r'^settings/system$', views.settings, name='settings'),
    # Settings -> Company
    url(r'^settings/company/edit$', views.company_edit, name='company_edit'),
    url(r'^settings/company$', views.company, name='company'),
    # Settings -> Contract
    url(r'^settings/contract/edit$',
        views.contract_settings_edit,
        name='contract_settings_edit'),
    url(r'^settings/contract$',
        views.contract_settings,
        name='contract_settings'),
    # Social
    url('', include(
        'django.contrib.auth.urls', namespace='auth')),
    url('', include(
        'social_django.urls', namespace='social')),
    # Task
    url(r'^task/(?P<pk>\d+)$', views.task, name='task'),
    url(r'^task/(?P<pk>\d+)/edit$', views.task_edit, name='task_edit'),
    url(r'^task/add$', views.task_edit, name='task_edit'),
    url(r'^task$', views.task_index, name='task_index'),
    # Time
    url(r'^time/(?P<pk>\d+)$', views.time, name='entry'),
    url(r'^time/(?P<pk>\d+)/edit$', views.time_edit, name='entry_edit'),
    url(r'^time/add$', views.time_edit, name='entry_edit'),
    url(r'^time$', views.time_index, name='entry_index'),
    # User
    url(r'^user/(?P<pk>\d+)$', views.user, name='user'),
    url(r'^user/(?P<pk>\d+)/edit$', views.user_edit, name='user_edit'),
    url(r'^user/(?P<pk>\d+)/contact$', views.user_contact,
        name='user_contact'),
    url(r'^user$', views.user_index, name='user_index'),
]
