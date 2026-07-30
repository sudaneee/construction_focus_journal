from website.models import Submission


def pending_submissions_count(request):
    if not request.path.startswith('/dashboard/') or not request.user.is_authenticated:
        return {}
    return {
        'pending_submissions_count': Submission.objects.filter(status=Submission.STATUS_PENDING).count(),
    }
