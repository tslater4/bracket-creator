from django.shortcuts import render

# Create your views here.

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django import forms
from django.forms import inlineformset_factory, modelformset_factory
from .models import TournamentBracket, Participant


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

class BracketListView(LoginRequiredMixin, ListView):
    model = TournamentBracket
    template_name = 'bracket/bracket_list.html'
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

class TournamentBracketForm(forms.ModelForm):
    class Meta:
        model = TournamentBracket
        fields = ['name', 'size']

ParticipantFormSet = inlineformset_factory(
    TournamentBracket,
    Participant,
    fields=['name'],
    extra=4, 
    can_delete=False
)

class BracketCreateView(LoginRequiredMixin, CreateView):
    model = TournamentBracket
    form_class = TournamentBracketForm
    template_name = 'bracket/bracket_form.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        return redirect('participant-add', bracket_pk=self.object.pk)

class ParticipantCreateView(LoginRequiredMixin, CreateView):
    template_name = 'bracket/participant_form.html'

    def get(self, request, bracket_pk):
        bracket = TournamentBracket.objects.get(pk=bracket_pk, user=request.user)
        ParticipantFormSet = modelformset_factory(
            Participant,
            fields=['name'],
            extra=bracket.size,
            max_num=bracket.size,
            validate_max=True,
            can_delete=False
        )
        formset = ParticipantFormSet(queryset=Participant.objects.none())
        return render(request, self.template_name, {'formset': formset, 'bracket': bracket})

    def post(self, request, bracket_pk):
        bracket = TournamentBracket.objects.get(pk=bracket_pk, user=request.user)
        ParticipantFormSet = modelformset_factory(
            Participant,
            fields=['name'],
            extra=bracket.size,
            max_num=bracket.size,
            validate_max=True,
            can_delete=False
        )
        formset = ParticipantFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data.get('name'):
                    Participant.objects.create(
                        name=form.cleaned_data['name'],
                        bracket=bracket
                    )
            return redirect('bracket-detail', pk=bracket.pk)
        return render(request, self.template_name, {'formset': formset, 'bracket': bracket})

class BracketDetailView(LoginRequiredMixin, DetailView):
    model = TournamentBracket
    template_name = 'bracket/bracket_detail.html'
    
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['participants'] = self.object.participants.all()
        return context
    
class BracketDeleteView(LoginRequiredMixin, DeleteView):
    model = TournamentBracket
    success_url = reverse_lazy('bracket-list')

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
    

class BracketUpdateView(LoginRequiredMixin, View):
    template_name = 'bracket/update_form.html'

    def get(self, request, bracket_pk):
        bracket = TournamentBracket.objects.get(pk=bracket_pk, user=request.user)
        bracket_form = TournamentBracketForm(instance=bracket)
        ParticipantFormSet = modelformset_factory(
            Participant,
            fields=['name'],
            extra=0,
            can_delete=True
        )
        formset = ParticipantFormSet(queryset=Participant.objects.filter(bracket=bracket).order_by('id'))
        return render(request, self.template_name, {
            'formset': formset,
            'bracket_form': bracket_form,
            'bracket': bracket
        })

    def post(self, request, bracket_pk):
        bracket = TournamentBracket.objects.get(pk=bracket_pk, user=request.user)
        bracket_form = TournamentBracketForm(request.POST, instance=bracket)
        ParticipantFormSet = modelformset_factory(
            Participant,
            fields=['name'],
            extra=0,
            can_delete=True
        )
        formset = ParticipantFormSet(request.POST, queryset=Participant.objects.filter(bracket=bracket).order_by('id'))
        if bracket_form.is_valid() and formset.is_valid():
            bracket_form.save()
            instances = formset.save(commit=False)
            for instance in instances:
                instance.bracket = bracket
                instance.save()
            for obj in formset.deleted_objects:
                obj.delete()
            return redirect('bracket-detail', pk=bracket.pk)
        return render(request, self.template_name, {
            'formset': formset,
            'bracket_form': bracket_form,
            'bracket': bracket
        })