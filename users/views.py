import logging
import datetime
from django import contrib
from django.contrib import messages
from django.core.mail import send_mail
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import generic
from agents.mixins import OrganisorAndLoginRequiredMixin
from .models import Patient, Agent, Category, FollowUp
from .forms import (
    PatientModelForm, 
    CustomUserCreationForm, 
    AssignAgentForm, 
    PatientCategoryUpdateForm,
    CategoryModelForm,
    FollowUpModelForm
)


logger = logging.getLogger(__name__)


# CRUD+L - Create, Retrieve, Update and Delete + List


class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")

class LandingPageView(generic.TemplateView):
    template_name = "landing.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard")
        return super().dispatch(request, *args, **kwargs)


class DashboardView(OrganisorAndLoginRequiredMixin, generic.TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        user = self.request.user

        # How many patients we have in total
        total_patient_count = Patient.objects.filter(organisation=user.userprofile).count()

        # How many new patients in the last 30 days
        thirty_days_ago = datetime.date.today() - datetime.timedelta(days=30)

        total_in_past30 = Patient.objects.filter(
            organisation=user.userprofile,
            date_added__gte=thirty_days_ago
        ).count()

        # How many contacted patients in the last 30 days
        contacted_category = Category.objects.get(name="Contacted")
        contacted_in_past30 = Patient.objects.filter(
            organisation=user.userprofile,
            category=contacted_category,
            contacted_date__gte=thirty_days_ago
        ).count()

        context.update({
            "total_patient_count": total_patient_count,
            "total_in_past30": total_in_past30,
            "contacted_in_past30": contacted_in_past30
        })
        return context


def landing_page(request):
    return render(request, "landing.html")


class PatientListView(OrganisorAndLoginRequiredMixin, generic.ListView):
    template_name = "patients/patient_list.html"
    context_object_name = "patients"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of patients for the entire organisation
        if user.is_organisor:
            queryset = Patient.objects.filter(
                organisation=user.userprofile, 
                agent__isnull=False
            )
        else:
            queryset = Patient.objects.filter(
                organisation=user.agent.organisation, 
                agent__isnull=False
            )
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PatientListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            queryset = Patient.objects.filter(
                organisation=user.userprofile, 
                agent__isnull=True
            )
            context.update({
                "unassigned_patients": queryset
            })
        return context


def patient_list(request):
    patients = Patient.objects.all()
    context = {
        "patients": patients
    }
    return render(request, "patients/patient_list.html", context)


class PatientDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "patients/patient_detail.html"
    context_object_name = "patient"
    
    def get_queryset(self):
        user = self.request.user
        # initial queryset of patients for the entire organisation
        if user.is_organisor:
            queryset = Patient.objects.filter(organisation=user.userprofile)
        else:
            queryset = Patient.objects.filter(organisation=user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset


def patient_detail(request, pk):
    patient = Patient.objects.get(id=pk)
    context = {
        "patient": patient
    }
    return render(request, "patients/patient_detail.html", context)


class PatientCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "patients/patient_create.html"
    form_class = PatientModelForm

    def get_success_url(self):
        return reverse("patients:patient-list")

    def form_valid(self, form):
        patient = form.save(commit=False)
        patient.organisation = self.request.user.userprofile
        patient.save()
        send_mail(
            subject="A patient has been created",
            message="Go to the site to see the new patient",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        messages.success(self.request, "You have successfully created a patient")
        return super(PatientCreateView, self).form_valid(form)


def patient_create(request):
    form = PatientModelForm()
    if request.method == "POST":
        form = PatientModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/patients")
    context = {
        "form": form
    }
    return render(request, "patients/patient_create.html", context)


class PatientUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "patients/patient_update.html"
    form_class = PatientModelForm

    def get_queryset(self):
        user = self.request.user
        # initial queryset of patients for the entire organisation
        return Patient.objects.filter(organisation=user.userprofile)

    def get_success_url(self):
        return reverse("patients:patient-list")

    def form_valid(self, form):
        form.save()
        messages.info(self.request, "You have successfully updated this patient")
        return super(PatientUpdateView, self).form_valid(form)


def patient_update(request, pk):
    patient = Patient.objects.get(id=pk)
    form = PatientModelForm(instance=patient)
    if request.method == "POST":
        form = PatientModelForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect("/patients")
    context = {
        "form": form,
        "patient": patient
    }
    return render(request, "patients/patient_update.html", context)


class PatientDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "patients/patient_delete.html"

    def get_success_url(self):
        return reverse("patients:patient-list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of patients for the entire organisation
        return Patient.objects.filter(organisation=user.userprofile)


def patient_delete(request, pk):
    patient = Patient.objects.get(id=pk)
    patient.delete()
    return redirect("/patients")


class AssignAgentView(OrganisorAndLoginRequiredMixin, generic.FormView):
    template_name = "patients/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs
        
    def get_success_url(self):
        return reverse("patients:patient-list")

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        patient = Patient.objects.get(id=self.kwargs["pk"])
        patient.agent = agent
        patient.save()
        return super(AssignAgentView, self).form_valid(form)


class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = "patients/category_list.html"
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_organisor:
            queryset = Patient.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Patient.objects.filter(
                organisation=user.agent.organisation
            )

        context.update({
            "unassigned_patient_count": queryset.filter(category__isnull=True).count()
        })
        return context

    def get_queryset(self):
        user = self.request.user
        # initial queryset of patients for the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset


class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "patients/category_detail.html"
    context_object_name = "category"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of patients for the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset


class CategoryCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "patients/category_create.html"
    form_class = CategoryModelForm

    def get_success_url(self):
        return reverse("patients:category-list")

    def form_valid(self, form):
        category = form.save(commit=False)
        category.organisation = self.request.user.userprofile
        category.save()
        return super(CategoryCreateView, self).form_valid(form)


class CategoryUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "patients/category_update.html"
    form_class = CategoryModelForm

    def get_success_url(self):
        return reverse("patients:category-list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of patients for the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset


class CategoryDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "patients/category_delete.html"

    def get_success_url(self):
        return reverse("patients:category-list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of patients for the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset


class patientCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "patients/patient_category_update.html"
    form_class = PatientCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user
        # initial queryset of patients for the entire organisation
        if user.is_organisor:
            queryset = Patient.objects.filter(organisation=user.userprofile)
        else:
            queryset = Patient.objects.filter(organisation=user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse("patients:patient-detail", kwargs={"pk": self.get_object().id})

    def form_valid(self, form):
        patient_before_update = self.get_object()
        instance = form.save(commit=False)
        contacted_category = Category.objects.get(name="contacted")
        if form.cleaned_data["category"] == contacted_category:
            # update the date at which this patient was contacted
            if patient_before_update.category != contacted_category:
                # this patient has now been contacted
                instance.contacted_date = datetime.datetime.now()
        instance.save()
        return super(patientCategoryUpdateView, self).form_valid(form)


class FollowUpCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "patients/followup_create.html"
    form_class = FollowUpModelForm

    def get_success_url(self):
        return reverse("patients:patient-detail", kwargs={"pk": self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        context = super(FollowUpCreateView, self).get_context_data(**kwargs)
        context.update({
            "patient": Patient.objects.get(pk=self.kwargs["pk"])
        })
        return context

    def form_valid(self, form):
        patient = Patient.objects.get(pk=self.kwargs["pk"])
        followup = form.save(commit=False)
        followup.patient = patient
        followup.save()
        return super(FollowUpCreateView, self).form_valid(form)


class FollowUpUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "patients/followup_update.html"
    form_class = FollowUpModelForm

    def get_queryset(self):
        user = self.request.user
        # initial queryset of patients for the entire organisation
        if user.is_organisor:
            queryset = FollowUp.objects.filter(patient__organisation=user.userprofile)
        else:
            queryset = FollowUp.objects.filter(patient__organisation=user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(patient__agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse("patients:patient-detail", kwargs={"pk": self.get_object().patient.id})


class FollowUpDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "patients/followup_delete.html"

    def get_success_url(self):
        followup = FollowUp.objects.get(id=self.kwargs["pk"])
        return reverse("patients:patient-detail", kwargs={"pk": followup.patient.pk})

    def get_queryset(self):
        user = self.request.user
        # initial queryset of patients for the entire organisation
        if user.is_organisor:
            queryset = FollowUp.objects.filter(patient__organisation=user.userprofile)
        else:
            queryset = FollowUp.objects.filter(patient__organisation=user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(patient__agent__user=user)
        return queryset
    

class PatientJsonView(generic.View):
    
    def get(self, request, *args, **kwargs):
        
        qs = list(Patient.objects.all().values(
            "first_name", 
            "last_name", 
            "agent",
            "organisation",
            "status",
            "categories",)
        )

        return JsonResponse({
            "qs": qs,
        })



