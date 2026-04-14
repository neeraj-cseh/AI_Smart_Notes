from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Note
from .forms import NoteForm
from .services.ai_service import summarize_text


@login_required
def home(request):
    notes = Note.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notes/home.html', {'notes': notes})


@login_required
def create_note(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('home')
    else:
        form = NoteForm()

    return render(request, 'notes/create_note.html', {'form': form})


@login_required
def summarize_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)

    try:
        summary = summarize_text(note.content)
        note.summary = summary
        note.save()
        messages.success(request, "Summary generated!")

    except Exception as e:
        messages.error(request, str(e))

    return redirect('home')