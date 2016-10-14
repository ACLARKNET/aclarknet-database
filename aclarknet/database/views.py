from .forms import ClientForm
from .forms import CompanyForm
from .forms import ContactForm
from .forms import EstimateForm
from .forms import InvoiceForm
from .forms import MailForm
from .forms import ProfileForm
from .forms import ProjectForm
from .forms import ReportForm
from .forms import TaskForm
from .models import Client
from .models import Company
from .models import Contact
from .models import Estimate
from .models import Invoice
from .models import Profile
from .models import Project
from .models import Report
from .models import Service
from .models import Testimonial
from .models import Task
from .models import Time
from .serializers import ClientSerializer
from .serializers import ProfileSerializer
from .serializers import ServiceSerializer
from .serializers import TestimonialSerializer
from .utils import active_status
from .utils import add_user_to_contacts
from .utils import daily_burn
from .utils import dashboard_items
from .utils import dashboard_totals
from .utils import edit
from .utils import entries_total
from .utils import search
from .utils import send_mail
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import F, Sum
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django_xhtml2pdf.utils import generate_pdf
from rest_framework import viewsets

# Create your views here.


class ClientViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = Client.objects.filter(published=True).order_by('name')
    serializer_class = ClientSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = Service.objects.filter(active=True).order_by('name')
    serializer_class = ServiceSerializer


class TestimonialViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = Testimonial.objects.filter(active=True).order_by('-issue_date')
    serializer_class = TestimonialSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = Profile.objects.filter(active=True).order_by('user__first_name')
    serializer_class = ProfileSerializer


# http://stackoverflow.com/a/24817024
def certbot(request):
    return HttpResponse(
        "sDCP-vgBF1OCR9Li6hiOx9qEuHGg1O2fFgpvzvT32IE.6xThCuQTIxsbemzNAhijnalO8y0T07rvXof2ZC8c4EM")


@staff_member_required
def client(request, pk=None):
    context = {}
    client = get_object_or_404(Client, pk=pk)

    contacts = Contact.objects.filter(client=client, active=True)
    contacts = contacts.order_by('-pk')

    projects = Project.objects.filter(client=client)
    projects = projects.order_by('-start_date')

    context['client'] = client
    context['contacts'] = contacts
    context['projects'] = projects

    return render(request, 'client.html', context)


@staff_member_required
def client_edit(request, pk=None):
    kwargs = {}
    url_name = 'client_index'
    if pk:
        kwargs['pk'] = pk
        url_name = 'client'
    return edit(
        request,
        ClientForm,
        Client,
        url_name,
        'client_edit.html',
        kwargs=kwargs,
        pk=pk)


@staff_member_required
def client_index(request):
    context = {}
    active = active_status(request)
    fields = ('address', 'name')
    order_by = '-pk'
    context, items = search(
        request,
        Client,
        fields,
        active=active,
        order_by=order_by,
        context=context)
    context['active'] = active
    context['edit_url'] = 'client_edit'  # Delete form modal
    context['items'] = items
    return render(request, 'client_index.html', context)


@staff_member_required
def company_edit(request, pk=None):
    return edit(
        request, CompanyForm, Company, 'company', 'company_edit.html', pk=1)


@staff_member_required
def company(request):
    context = {}
    company = Company.get_solo()
    context['company'] = company
    return render(request, 'company.html', context)


@staff_member_required
def contact(request, pk=None):
    context = {}
    contact = get_object_or_404(Contact, pk=pk)
    context['contact'] = contact
    return render(request, 'contact.html', context)


@staff_member_required
def contact_edit(request, pk=None):
    url_name = 'contact_index'
    kwargs = {}
    if pk:
        kwargs['pk'] = pk
        url_name = 'contact'
    client = request.GET.get('client')
    if client:
        client = get_object_or_404(Client, pk=client)
        url_name = 'client_index'
    return edit(
        request,
        ContactForm,
        Contact,
        url_name,
        'contact_edit.html',
        client=client,
        kwargs=kwargs,
        pk=pk)


@staff_member_required
def contact_index(request):
    context = {}
    active = active_status(request)
    fields = ('first_name', 'last_name', 'email', 'notes')
    order_by = '-pk'
    context, items = search(
        request,
        Contact,
        fields,
        active=active,
        order_by=order_by,
        context=context)
    context['active'] = active
    context['edit_url'] = 'contact_edit'  # Delete form modal
    context['items'] = items
    return render(request, 'contact_index.html', context)


@staff_member_required
def contact_mail(request, pk=None):
    context = {}
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        form = MailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            send_mail(subject, message, contact.email)
            messages.add_message(request, messages.SUCCESS, 'Message sent!')
            return HttpResponseRedirect(reverse('contact_index'))
    else:
        form = MailForm()
    context['form'] = form
    context['contact'] = contact
    return render(request, 'contact_mail.html', context)


@staff_member_required
def estimate(request, pk=None):
    context = {}

    company = Company.get_solo()
    if company:
        context['company'] = company

    estimate = get_object_or_404(Estimate, pk=pk)

    document_id = str(estimate.document_id)
    document_type = estimate._meta.verbose_name
    document_type_upper = document_type.upper()
    document_type_title = document_type.title()

    context['document'] = estimate
    context['document_type_upper'] = document_type_upper
    context['document_type_title'] = document_type_title

    times_client = Time.objects.filter(
        client=estimate.client,
        estimate=None,
        project=None,
        invoiced=False,
        invoice=None)
    times_estimate = Time.objects.filter(estimate=estimate)
    times = times_client | times_estimate
    times = times.order_by('-date')

    entries, subtotal, paid_amount, hours, amount = entries_total(times)
    context['entries'] = entries
    context['amount'] = amount
    context['paid_amount'] = paid_amount
    context['subtotal'] = subtotal
    context['hours'] = hours

    pdf = request.GET.get('pdf')
    context['pdf'] = pdf
    if pdf:
        company_name = ''
        if company.name:
            company_name = company.name.replace('.', '_')
            company_name = company_name.replace(', ', '_')
            company_name = company_name.upper()
        response = HttpResponse(content_type='application/pdf')
        filename = '_'.join([document_type_upper, document_id, company_name])
        response['Content-Disposition'] = 'filename=%s.pdf' % filename
        return generate_pdf(
            'invoice_table.html', context=context, file_object=response)
    else:
        return render(request, 'estimate.html', context)


@staff_member_required
def estimate_edit(request, pk=None):
    amount = request.GET.get('amount')
    paid_amount = request.GET.get('paid_amount')
    subtotal = request.GET.get('subtotal')
    times = request.GET.get('times')
    company = Company.get_solo()

    if times:
        estimate = get_object_or_404(Estimate, pk=pk)
        times = Time.objects.filter(pk__in=[int(i) for i in times.split(',')])
        for entry in times:
            entry.estimate = estimate
            entry.save()

    return edit(
        request,
        EstimateForm,
        Estimate,
        'estimate_index',
        'estimate_edit.html',
        amount=amount,
        paid_amount=paid_amount,
        pk=pk,
        subtotal=subtotal,
        company=company)


@staff_member_required
def estimate_index(request):
    context = {}
    company = Company.get_solo()
    fields = ('subject', )
    order_by = '-issue_date'
    context, items = search(request, Estimate, fields, order_by=order_by)
    context['active'] = active_status(request)
    context['edit_url'] = 'estimate_edit'  # Delete form modal
    context['items'] = items
    context['company'] = company
    return render(request, 'estimate_index.html', context)


def home(request):
    context = {}
    company = Company.get_solo()
    gross, net = dashboard_totals(Invoice)
    items = dashboard_items(Project, order_by='client__name')
    # http://stackoverflow.com/a/35044521
    for item in items:
        item.daily_burn = daily_burn(item)
    invoices = Invoice.objects.filter(
        last_payment_date=None).order_by('amount')
    context['data_visible'] = 'false'  # Hide some items
    context['edit_url'] = 'project_edit'  # Delete form modal
    context['company'] = company
    context['gross'] = gross
    context['invoices'] = invoices
    context['items'] = items  # projects
    context['net'] = net
    return render(request, 'dashboard.html', context)


@staff_member_required
def invoice(request, pk=None):
    context = {}

    company = Company.get_solo()
    if company:
        context['company'] = company

    invoice = get_object_or_404(Invoice, pk=pk)

    document_id = str(invoice.document_id)
    document_type = invoice._meta.verbose_name
    document_type_upper = document_type.upper()
    document_type_title = document_type.title()

    context['document'] = invoice
    context['document_type_upper'] = document_type_upper
    context['document_type_title'] = document_type_title

    times_project = Time.objects.filter(
        invoiced=False, project=invoice.project, estimate=None, invoice=None)
    times_invoice = Time.objects.filter(invoice=invoice)
    times = times_project | times_invoice
    times = times.order_by('-date')

    entries, subtotal, paid_amount, hours, amount = entries_total(times)

    context['entries'] = entries
    context['amount'] = amount
    context['paid_amount'] = paid_amount
    context['subtotal'] = subtotal
    context['hours'] = hours

    context['invoice'] = True

    pdf = request.GET.get('pdf')
    context['pdf'] = pdf
    if pdf:
        response = HttpResponse(content_type='application/pdf')
        if company.name:
            company_name = company.name.replace('.', '_')
            company_name = company_name.replace(', ', '_')
            company_name = company_name.upper()
        else:
            company_name = 'COMPANY'
        filename = '_'.join([document_type_upper, document_id, company_name])
        response['Content-Disposition'] = 'filename=%s.pdf' % filename
        return generate_pdf(
            'invoice_table.html', context=context, file_object=response)
    else:
        return render(request, 'invoice.html', context)


@staff_member_required
def invoice_edit(request, pk=None):
    amount = request.GET.get('amount')
    paid_amount = request.GET.get('paid_amount')
    subtotal = request.GET.get('subtotal')
    times = request.GET.get('times')
    paid = request.GET.get('paid')
    company = Company.get_solo()
    project = request.GET.get('project')

    if project:
        project = get_object_or_404(Project, pk=project)

    if pk:
        invoice = get_object_or_404(Invoice, pk=pk)
        if invoice.project:
            if invoice.project.client and not invoice.client:
                invoice.client = invoice.project.client
                invoice.save()

    if paid and times:
        times = Time.objects.filter(pk__in=[int(i) for i in times.split(',')])
        for entry in times:
            entry.invoiced = True
            entry.save()
    elif times:
        invoice = get_object_or_404(Invoice, pk=pk)
        times = Time.objects.filter(pk__in=[int(i) for i in times.split(',')])
        for entry in times:
            entry.invoice = invoice
            entry.save()

    return edit(
        request,
        InvoiceForm,
        Invoice,
        'invoice_index',
        'invoice_edit.html',
        amount=amount,
        paid_amount=paid_amount,
        paid=paid,
        pk=pk,
        project=project,
        subtotal=subtotal,
        company=company)


@staff_member_required
def invoice_index(request):
    context = {}
    active = active_status(request)
    company = Company.get_solo()
    fields = ('client__name',
              'document_id',
              'issue_date',
              'project__name',
              'subject', )
    order_by = '-issue_date'
    context, items = search(
        request, Invoice, fields, active=active, order_by=order_by)
    context['active'] = active
    context['edit_url'] = 'invoice_edit'  # Delete form modal
    context['items'] = items
    context['company'] = company
    return render(request, 'invoice_index.html', context)


@staff_member_required
def project(request, pk=None):
    context = {}
    project = get_object_or_404(Project, pk=pk)
    times = Time.objects.filter(
        project=project, invoiced=False).order_by('-date')
    invoices = Invoice.objects.filter(project=project, last_payment_date=None)
    context['company'] = Company.get_solo()
    context['data_visible'] = 'false'  # Hide some items
    context['project'] = project
    context['edit_url'] = 'entry_edit'  # Delete form modal
    context['items'] = times
    context['invoices'] = invoices
    context['daily_burn'] = daily_burn(project)
    return render(request, 'project.html', context)


@staff_member_required
def project_edit(request, pk=None):
    url_name = 'project_index'
    kwargs = {}
    clients = []
    if pk:
        kwargs['pk'] = pk
        url_name = 'project'
    else:
        clients = Client.objects.filter(active=True)
    client = request.GET.get('client')
    if client:
        client = get_object_or_404(Client, pk=client)
        url_name = 'client_index'
    return edit(
        request,
        ProjectForm,
        Project,
        url_name,
        'project_edit.html',
        client=client,
        clients=clients,
        kwargs=kwargs,
        pk=pk)


@staff_member_required
def project_index(request, pk=None):
    context = {}
    active = active_status(request)
    fields = ('id', 'name')
    order_by = '-start_date'
    context, items = search(
        request,
        Project,
        fields,
        active=active,
        order_by=order_by,
        context=context)
    context['active'] = active
    context['data_visible'] = 'true'  # Show all items
    context['edit_url'] = 'project_edit'  # Delete form modal
    context['items'] = items
    return render(request, 'project_index.html', context)


@staff_member_required
def report(request, pk=None):
    context = {}
    report = get_object_or_404(Report, pk=pk)
    context['report'] = report
    context['diff'] = report.gross - report.net
    return render(request, 'report.html', context)


@staff_member_required
def report_index(request):
    context = {}
    company = Company.get_solo()
    items = Report.objects.all().annotate(diff=F('gross') - F('net'))
    agg = Report.objects.aggregate(gross=Sum(F('gross')), net=Sum(F('net')))
    if agg['gross'] is not None and agg['net'] is not None:
        diff = agg['gross'] - agg['net']
    else:
        agg['gross'] = 0
        agg['net'] = 0
        diff = 0
    context['items'] = items
    context['agg'] = agg
    context['company'] = company
    context['diff'] = diff
    context['edit_url'] = 'report_edit'  # Delete form modal
    return render(request, 'report_index.html', context)


@staff_member_required
def report_edit(request, pk=None):
    gross, net = dashboard_totals(Invoice)
    return edit(
        request,
        ReportForm,
        Report,
        'report_index',
        'report_edit.html',
        gross=gross,
        net=net,
        pk=pk)


@staff_member_required
def task(request, pk=None):
    context = {}
    task = get_object_or_404(Task, pk=pk)
    context['task'] = task
    return render(request, 'task.html', context)


@staff_member_required
def task_edit(request, pk=None):
    kwargs = {}
    url_name = 'task_index'
    if pk:
        kwargs['pk'] = pk
        url_name = 'task'
    return edit(
        request,
        TaskForm,
        Task,
        url_name,
        'task_edit.html',
        pk=pk,
        kwargs=kwargs)


@staff_member_required
def task_index(request):
    context = {}
    active = active_status(request)
    order_by = '-pk'
    fields = ('name', )
    context, items = search(
        request,
        Task,
        fields,
        active=active,
        order_by=order_by,
        context=context)
    context['active'] = active
    context['edit_url'] = 'task_edit'  # Delete form modal
    context['items'] = items
    return render(request, 'task_index.html', context)


@login_required
def time(request, pk=None):
    context = {}
    entry = get_object_or_404(Time, pk=pk)
    if not entry.user and not request.user.is_staff:
        return HttpResponseRedirect(reverse('admin:index'))
    if entry.user:
        if (not entry.user.username == request.user.username and
                not request.user.is_staff):
            return HttpResponseRedirect(reverse('admin:index'))
    context['entry'] = entry
    return render(request, 'time.html', context)


@login_required
def time_edit(request, pk=None):
    if pk is not None:
        entry = get_object_or_404(Time, pk=pk)
        if entry.user:
            if (entry.user.username != request.user.username and
                    not request.user.is_staff):
                return HttpResponseRedirect(reverse('admin:index'))
        else:
            if not request.user.is_staff:
                return HttpResponseRedirect(reverse('admin:index'))

    url_name = 'entry_index'
    kwargs = {}

    if pk:
        kwargs['pk'] = pk
        url_name = 'entry'

    client = request.GET.get('client')
    project = request.GET.get('project')

    task = None

    if client:
        client = get_object_or_404(Client, pk=client)

    if project:
        project = get_object_or_404(Project, pk=project)

        if project.task:
            task = get_object_or_404(Task, pk=project.task.pk)

    projects = Project.objects.filter(team=request.user.pk)
    clients = Client.objects.filter(
        pk__in=[i.client.pk for i in projects if i.client])
    tasks = Task.objects.filter(pk__in=[i.task.pk for i in projects if i.task])

    if request.user.is_staff:
        from .forms import TimeAdminForm as TimeForm
    else:
        from .forms import TimeForm

    return edit(
        request,
        TimeForm,
        Time,
        url_name,
        'time_edit.html',
        client=client,
        clients=clients,
        pk=pk,
        project=project,
        projects=projects,
        task=task,
        tasks=tasks,
        kwargs=kwargs)


@login_required
def time_index(request):
    context = {}
    active = active_status(request)
    fields = ('client__name', 'date', 'notes', 'pk', 'project__name',
              'invoice__document_id', 'user__username')
    order_by = '-pk'
    context, items = search(
        request,
        Time,
        fields,
        active=active,
        order_by=order_by,
        context=context)
    context['active'] = active
    context['data_visible'] = 'true'  # Show all items
    context['edit_url'] = 'entry_edit'  # Delete form modal
    context['items'] = items
    return render(request, 'time_index.html', context)


@login_required
def user(request, pk=None):
    context = {}
    company = Company.get_solo()
    user = get_object_or_404(User, pk=pk)
    profile = Profile.objects.get_or_create(user=user)[0]
    times = Time.objects.filter(user=user, estimate=None, invoiced=False)
    total_hours = times.aggregate(hours=Sum(F('hours')))
    total_hours = total_hours['hours']
    if profile.rate and total_hours:
        total_dollars = profile.rate * total_hours
    else:
        total_dollars = 0
    context['company'] = company
    context['edit_url'] = 'entry_edit'  # Delete form modal
    context['profile'] = profile
    context['request'] = request
    context['user'] = user
    context['items'] = times
    context['total_hours'] = total_hours
    context['total_dollars'] = '%.2f' % total_dollars
    if request.user.pk == int(pk) or request.user.is_staff:
        return render(request, 'user.html', context)
    else:
        return HttpResponseRedirect(reverse('home'))


@staff_member_required
def user_contact(request, pk=None):
    return add_user_to_contacts(request, Contact, pk=pk)


@login_required
def user_edit(request, pk=None):
    context = {}
    user = get_object_or_404(User, pk=pk)
    context['user'] = user
    return edit(
        request,
        ProfileForm,
        Profile,
        'home',
        'user_edit.html',
        pk=pk,
        context=context)


@staff_member_required
def user_index(request):
    context = {}
    active = active_status(request)
    company = Company.get_solo()
    fields = ('first_name', 'last_name', 'email')
    context, items = search(
        request, User, fields, active=active, context=context)
    context['active'] = active
    context['items'] = items
    context['company'] = company
    return render(request, 'user_index.html', context)
