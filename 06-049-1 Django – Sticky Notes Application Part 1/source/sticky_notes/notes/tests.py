# notes/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from .models import Note


class NoteModelTests(TestCase):
    """Unit tests for the Note model."""

    def test_create_note(self):
        """Test note creation and string representation."""
        note = Note.objects.create(
            title="Meeting Notes",
            content="Discuss project roadmap and timelines."
        )
        self.assertEqual(note.title, "Meeting Notes")
        self.assertEqual(note.content, "Discuss project roadmap and timelines.")
        self.assertEqual(str(note), "Meeting Notes")
        self.assertIsNotNone(note.created_at)


class NoteViewTests(TestCase):
    """Unit tests for the CRUD views."""

    def setUp(self):
        self.client = Client()
        self.note = Note.objects.create(
            title="Test Note",
            content="Sample content for testing."
        )

    def test_note_list_view(self):
        """Test listing sticky notes."""
        response = self.client.get(reverse('note_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/note_list.html')
        self.assertContains(response, "Test Note")

    def test_note_detail_view(self):
        """Test viewing single sticky note details."""
        response = self.client.get(reverse('note_detail', kwargs={'pk': self.note.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/note_detail.html')
        self.assertContains(response, "Test Note")
        self.assertContains(response, "Sample content for testing.")

    def test_note_create_view_get(self):
        """Test displaying note creation form."""
        response = self.client.get(reverse('note_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/note_form.html')

    def test_note_create_view_post(self):
        """Test submitting note creation form."""
        response = self.client.post(reverse('note_create'), {
            'title': 'New Created Note',
            'content': 'Content of the new note.'
        })
        self.assertRedirects(response, reverse('note_list'))
        self.assertTrue(Note.objects.filter(title='New Created Note').exists())

    def test_note_update_view(self):
        """Test updating an existing note."""
        response = self.client.post(
            reverse('note_update', kwargs={'pk': self.note.pk}),
            {
                'title': 'Updated Title',
                'content': 'Updated content body.'
            }
        )
        self.assertRedirects(response, reverse('note_list'))
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Updated Title')
        self.assertEqual(self.note.content, 'Updated content body.')

    def test_note_delete_view(self):
        """Test deleting a note."""
        response = self.client.get(reverse('note_delete', kwargs={'pk': self.note.pk}))
        self.assertRedirects(response, reverse('note_list'))
        self.assertFalse(Note.objects.filter(pk=self.note.pk).exists())
