from django.shortcuts import render

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

# Create your views here.

from blog.models import Post
from .forms import CommentForm


@require_POST
def comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    form = CommentForm(request.POST)

    if form.is_valid():

        # Commit =False is used to simply generate an instance of the Comment model class from the form's data,
        # but does not yet save the Comment data to the database.
        comment = form.save(commit=False)

        # Associate the comment with the article being commented on.
        comment.post = post

        # Finally saves the comment data to the database and calls the save method of the model instance
        comment.save()

        messages.add_message(request, messages.SUCCESS, 'Success!', extra_tags='success')

        # Redirect to the Detail page of the Post,
        # which in fact calls the get_absolute_URL method of the model instance.
        # When the Redirect function receives an instance of the model,
        # then redirect to the URL returned by the get_absolute_URL method.
        return redirect(post)

    # After checking that the data is not valid, we render a preview page to show the error of the form.
    # Note that the post that was commented on here is also passed to the template
    # because we need to generate the submission address of the form based on post.
    context = {
        'post': post,
        'form': form,
    }
    messages.add_message(request, messages.ERROR, 'ERROR！Please modify the errors in the form and resubmit.', extra_tags='danger')
    return render(request, 'comments/preview.html', context=context)


