from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
#from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from pollstation.models import Choice, Poll


#def index(request):
#    latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
#    template = loader.get_template('pollstation/index.html')
#    context = RequestContext (request, {
#        'latest_poll_list': latest_poll_list,
#    })
#    return HttpResponse(template.render(context))

#def index(request):
#    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
#    context = {'latest_poll_list': latest_poll_list}
#    return	render(request, 'pollstation/index.html', context)

class IndexView(generic.ListView):
    template_name = 'pollstation/index.html'
    context_object_name = 'latest_poll_list'
    
    def get_queryset(self):
        """Return the last five published pollstation. (not including those set to be published
        in the future) 
        """
        return Poll.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]
    
#def detail(request, poll_id):
#    return HttpResponse("You're looking at poll %s" %poll_id)

#def detail(request, poll_id):
#    try:
#        poll: Poll.objects.get(pk=poll_id):
#    except Poll.DoesNotExist:
#        raise Http404
#    return render(request, 'pollstation/detail.html', {'poll': poll})

#def detail(request, poll_id):
#    poll = get_object_or_404(Poll, pk=poll_id)
#    return render(request, 'pollstation/detail.html', {'poll': poll})

class DetailView(generic.DetailView):
    model = Poll
    template_name = 'pollstation/detail.html'
    
#def results(request, poll_id):
#    poll = get_object_or_404(Poll, pk=poll_id)
#    return render(request, 'pollstation/results.html', {'poll': poll})

class ResultsView(generic.DetailView):
    model = Poll
    template_name = 'pollstation/results.html'
    
    
#def vote(request, poll_id):
#    return HttpResponse("You're voting on poll %s." % poll_id)

def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'pollstation/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('pollstation:results', args=(p.id,)))
    


