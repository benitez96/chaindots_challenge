from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
import logging

from todos.models import Todo


logger = logging.getLogger(__name__)

def todos_page(request):

    logger.info('Entering todos_page view')

    completed_todos = Todo.objects.filter(completed = True).order_by('-id')
    logger.info('completed_todos: %s', len(completed_todos))

    uncompleted_todos = Todo.objects.filter(completed = False).order_by('-id')
    logger.info('uncompleted_todos: %s', len(uncompleted_todos))

    if request.method == 'POST':
        Todo.objects.create(name=request.POST['name'])
        return redirect('/')

    ctx = {'completed_todos': completed_todos, 'uncompleted_todos': uncompleted_todos}

    return render(request, 'index.html', ctx)


def todo_delete(request, pk):

    logger.info('Entering todo_delete view, id: %s', pk)

    todo = get_object_or_404(Todo, id=pk)

    logger.info('Deleting todo: %s', todo)
    todo.delete()

    return redirect('todos_page')

def todo_toggle_complete(request, pk):

    logger.info('Entering todo_toggle_complete view, id: %s', pk)

    todo = get_object_or_404(Todo, id=pk)
    todo.completed = not todo.completed
    todo.save()

    logger.info('Toggling todo: %s', todo)

    return redirect('todos_page')














# def todo_edit(request, todo_id):
#     todo = get_object_or_404(Todo, id=todo_id)

#     if request.method == 'PATCH':
#         todo.name = request.PATCH['name']

#     return redirect('todos_page')
