from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from sampleapp.forms import SampleForm
from sampleapp.models import Sample


def top(request):
    sampleapp = Sample.objects.all()
    context = {'sampleapp': sampleapp}
    return render(request, 'sampleapp/top.html', context)


@login_required
def sample_new(request):
    if request.method == 'POST':
        form = SampleForm(request.POST)
        if form.is_valid():
            sample = form.save(commit=False)
            sample.created_by = request.user
            sample.save()
            return redirect(sample_detail, sample_id=sample.pk)
    else:
        form = SampleForm()
    return render(request, 'sampleapp/sample_new.html', {'form': form})


@login_required
def sample_edit(request, sample_id):
    sample = get_object_or_404(Sample, pk=sample_id)
    if sample.created_by_id != request.user.id:
        return HttpResponseForbidden("このスニペットの編集は許可されていません。")

    if request.method == "POST":
        form = SampleForm(request.POST, instance=sample)
        if form.is_valid():
            form.save()
            return redirect('sample_detail', sample_id=sample_id)
    else:
        form = SampleForm(instance=sample)
    return render(request, 'sampleapp/sample_edit.html', {'form': form})


def sample_detail(request, sample_id):
    sample = get_object_or_404(Sample, pk=sample_id)
    return render(request, 'sampleapp/sample_detail.html', {'sample': sample})