from django.test import TestCase, Client
from django.urls import reverse
from .models import Todo

class TodoListViewTest(TestCase):

    def test_todo_list_view_status_code(self):
        response = self.client.get(reverse('todos_page'))
        self.assertEqual(response.status_code, 200)

    def test_todos_page_view_template(self):
        response = self.client.get(reverse('todos_page'))
        self.assertTemplateUsed(response, 'index.html')

    def test_todos_page_view_context(self):
        response = self.client.get(reverse('todos_page'))
        completed_todos = response.context['completed_todos'].count()
        uncompleted_todos = response.context['uncompleted_todos'].count()
        self.assertEqual(completed_todos + uncompleted_todos, 0)

    def test_todos_page_view_context_with_todos(self):

        todos = [
            Todo(name='Test 1', completed=False),
            Todo(name='Test 2', completed=True),
        ]
        Todo.objects.bulk_create(todos)

        response = self.client.get(reverse('todos_page'))

        completed_todos = response.context['completed_todos'].count()
        uncompleted_todos = response.context['uncompleted_todos'].count()

        self.assertEqual(completed_todos + uncompleted_todos, 2)


    def test_create_todo(self):

        todo_count = Todo.objects.count()
        self.client.post(reverse('todos_page'), {'name': 'Test todo'})
        self.assertEqual(Todo.objects.count(), todo_count + 1)


    def test_toggle_todo(self):

        todo = Todo.objects.create(name='Test todo', completed=False)
        self.client.get(reverse('todo_toggle_complete', args=[todo.id]))
        todo.refresh_from_db()

        self.assertEqual(todo.completed, True)

    def test_delete_todo(self):

        todo = Todo.objects.create(name='Test todo', completed=False)
        self.client.get(reverse('todo_delete', args=[todo.id]))
        self.assertEqual(Todo.objects.count(), 0)
