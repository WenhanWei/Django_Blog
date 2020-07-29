from datetime import timedelta
from django.test import TestCase
from .models import *


# -------------------------Test For Model-------------------------
class PostModelTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_superuser(
            username='admin',
            email='',
            password='admin')
        category = Category.objects.create(name='Test')
        self.post = Post.objects.create(
            title='Test title',
            text='Test text',
            text_rich='Test text_rich',
            category=category,
            author=user,
        )

    # Should be the title
    def test_str_representation(self):
        self.assertEqual(self.post.__str__(), self.post.title)

    def test_auto_populate_modified_date(self):
        self.assertIsNotNone(self.post.modified_date)

        old_post_modified_date = self.post.modified_date
        self.post.text = 'New text alter'
        self.post.text_rich = 'New text_rich alter'
        self.post.save()
        self.post.refresh_from_db()

        self.assertTrue(self.post.modified_date > old_post_modified_date)

    def test_auto_abstract(self):
        self.assertIsNotNone(self.post.abstract)
        self.assertTrue(0 < len(self.post.abstract) <= 50)

    def test_get_absolute_url(self):
        expected_url = reverse('blog:blog_detail', kwargs={'pk': self.post.pk})
        self.assertEqual(self.post.get_absolute_url(), expected_url)

    def test_increase_views(self):
        self.post.increase_views()
        self.post.refresh_from_db()
        self.assertEqual(self.post.views, 1)

        self.post.increase_views()
        self.post.refresh_from_db()
        self.assertEqual(self.post.views, 2)


# -------------------------Test For View-------------------------
class BlogDataTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username='admin',
            email='',
            password='admin'
        )

        # Category
        self.category1 = Category.objects.create(name='category1')
        self.category2 = Category.objects.create(name='category2')

        # Tag
        self.tag1 = Tag.objects.create(name='tag1')
        self.tag2 = Tag.objects.create(name='tag2')

        # Posts
        self.post1 = Post.objects.create(
            title='Post 1',
            text='Post1 text',
            category=self.category1,
            author=self.user,
        )
        self.post1.tags.add(self.tag1)
        self.post1.save()

        self.post2 = Post.objects.create(
            title='Post 2',
            text='Post2 text',
            category=self.category2,
            author=self.user,
            created_date=timezone.now() - timedelta(days=100)
        )


class CategoryViewTestCase(BlogDataTestCase):
    def setUp(self):
        super().setUp()
        self.url1 = reverse('blog:blog_category', kwargs={'pk': self.category1.pk})
        self.url2 = reverse('blog:blog_category', kwargs={'pk': self.category2.pk})

    def test_visit_a_nonexistent_category(self):
        url = reverse('blog:blog_category', kwargs={'pk': 100})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_without_any_post(self):
        Post.objects.all().delete()
        response = self.client.get(self.url2)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('blog/blog_index.html')
        self.assertContains(response, 'Currently Empty...')

    def test_with_posts(self):
        response = self.client.get(self.url1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('blog/blog_index.html')
        self.assertContains(response, self.post1.title)
        self.assertIn('post_list', response.context)
        self.assertEqual(response.context['post_list'].count(), 1)
        expected_qs = self.category1.post_set.all().order_by('-created_date')
        self.assertQuerysetEqual(response.context['post_list'], [repr(p) for p in expected_qs])


class TagViewTestCase(BlogDataTestCase):
    def setUp(self):
        super().setUp()
        self.url1 = reverse('blog:blog_tag', kwargs={'pk': self.tag1.pk})
        self.url2 = reverse('blog:blog_tag', kwargs={'pk': self.tag2.pk})

    def test_visit_a_nonexistent_tag(self):
        url = reverse('blog:blog_tag', kwargs={'pk': 100})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_without_any_post(self):
        Post.objects.all().delete()
        response = self.client.get(self.url2)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('blog/blog_index.html')
        self.assertContains(response, 'Currently Empty...')

    def test_with_posts(self):
        response = self.client.get(self.url1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('blog/blog_index.html')
        self.assertContains(response, self.post1.title)
        self.assertIn('post_list', response.context)
        self.assertEqual(response.context['post_list'].count(), 1)
        expected_qs = self.category1.post_set.all().order_by('-created_date')
        self.assertQuerysetEqual(response.context['post_list'], [repr(p) for p in expected_qs])


class PostDetailViewTestCase(BlogDataTestCase):
    def setUp(self):
        super().setUp()
        self.md_post = Post.objects.create(
            title='Markdown Test',
            text='#Head',
            category=self.category1,
            author=self.user,
        )
        self.url = reverse('blog:blog_detail', kwargs={'pk': self.md_post.pk})

    def test_good_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('blog/blog_detail.html')
        self.assertContains(response, self.md_post.title)
        self.assertIn('post', response.context)

    def test_visit_a_nonexistent_post(self):
        url = reverse('blog:blog_detail', kwargs={'pk': 100})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_increase_views(self):
        self.client.get(self.url)
        self.md_post.refresh_from_db()
        self.assertEqual(self.md_post.views, 1)

        self.client.get(self.url)
        self.md_post.refresh_from_db()
        self.assertEqual(self.md_post.views, 2)

    def test_markdown_set_toc(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'Article Directories')
        self.assertContains(response, self.md_post.title)
        post_template_var = response.context['post']
        self.assertHTMLEqual(post_template_var.toc, '<li><a href="#head">Head</li>')

