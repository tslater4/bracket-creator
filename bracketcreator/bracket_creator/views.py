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
from .models import TournamentBracket, Participant, Match
from django.http import JsonResponse


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
        rounds = (
            self.object.matches.all()
            .values_list('round', flat=True)
            .distinct()
            .order_by('round')
        )
        context['rounds'] = rounds
        if rounds:
            context['final_round'] = rounds.last()
        else:
            context['final_round'] = None
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
    
def startTournament(request, pk):
    if request.method == "POST" and request.user.is_authenticated:
        bracket = get_object_or_404(TournamentBracket, pk=pk, user=request.user)
        bracket.started = True
        bracket.save()
        participants = list(bracket.participants.all())
        created = 0
        for i in range(0, len(participants), 2):
            p1 = participants[i]
            p2 = participants[i+1] if i+1 < len(participants) else None
            Match.objects.get_or_create(
                bracket=bracket,
                round=1,
                player1=p1,
                player2=p2
            )
            created += 1
        return JsonResponse({'status': 'ok', 'created': created})
    return JsonResponse({'status': 'error'}, status=400)

def set_winner(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    winner_id = request.POST.get('winner')
    if winner_id:
        winner = get_object_or_404(Participant, id=winner_id)
        match.winner = winner
        match.save()
        bracket = match.bracket 
        current_round = match.round
        next_round = current_round + 1
        participant_ids = list(bracket.matches.filter(round=current_round).values_list('winner', flat=True))
        participants = list(Participant.objects.filter(id__in=participant_ids))

        if all(match.winner for match in bracket.matches.filter(round=current_round)):
            participants.sort(key=lambda p: participant_ids.index(p.id))
            for i in range(0, len(participants), 2):
                p1 = participants[i]
                p2 = participants[i+1] if i+1 < len(participants) else None
                Match.objects.get_or_create(
                    bracket=bracket,
                    round=next_round,
                    player1=p1,
                    player2=p2
                )
        match.save()
    return redirect('bracket-detail', pk=match.bracket.pk)