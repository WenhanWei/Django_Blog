from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Comment
from blog.models import Category, Post


class CommentDataTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username='admin',
            email='',
            password='admin'
        )
        self.category = Category.objects.create(name='Test')
        self.post = Post.objects.create(
            title='Test',
            text='Test',
            category=self.category,
            author=self.user,
        )


class CommentModelTestCase(CommentDataTestCase):
    def setUp(self):
        super().setUp()
        self.comment = Comment.objects.create(
            name='john',
            email='a@a.com',
            text='good',
            post=self.post,
        )

    def test_str_representation(self):
        self.assertEqual(self.comment.__str__(), 'john: good')


class CommentViewTestCase(CommentDataTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('comments:comment', kwargs={'post_pk': self.post.pk})

    def test_invalid_comment_data(self):
        invalid_data = {
            'email': 'invalid_email',
        }
        response = self.client.post(self.url, invalid_data)
        self.assertTemplateUsed(response, 'comments/preview.html')
        self.assertIn('post', response.context)
        self.assertIn('form', response.context)
        form = response.context['form']
        for field_name, errors in form.errors.items():
            for err in errors:
                self.assertContains(response, err)
        self.assertContains(response, 'ERROR！Please modify the errors in the form and resubmit.')

    def test_valid_comment_data(self):
        valid_data = {
            'name': 'john',
            'email': 'a@a.com',
            'text': 'good',
        }
        response = self.client.post(self.url, valid_data, follow=True)
        self.assertRedirects(response, self.post.get_absolute_url())
        self.assertContains(response, 'Success!')
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.first()
        self.assertEqual(comment.name, valid_data['name'])
        self.assertEqual(comment.text, valid_data['text'])
