from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import Task

# blueprint for tasks
tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
def home():
    # redirect root of this blueprint to tasks list
    return redirect(url_for('tasks.view_tasks'))
@tasks_bp.route('/tasks', methods=['GET'])
def view_tasks():
    if 'user' not in session:
        flash('Please log in to view your tasks.', 'warning')
        return redirect(url_for('auth.login'))
    
    tasks = Task.query.order_by(Task.id.desc()).all()

    # Count tasks by status
    pending_count = Task.query.filter_by(status='pending').count()
    working_count = Task.query.filter_by(status='working').count()
    done_count = Task.query.filter_by(status='done').count()

    return render_template(
        'tasks.html',
        tasks=tasks,
        pending_count=pending_count,
        working_count=working_count,
        done_count=done_count
    )


@tasks_bp.route('/add', methods=['POST'])
def add_task():
    # require login
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    title = request.form.get('title', '').strip()
    if title:
        new_task = Task(title=title, status='pending')
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully!', 'success')
    else:
        flash('Task title required.', 'danger')

    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_status(task_id):
    # require login
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    task = Task.query.get(task_id)
    if task:
        if task.status == 'pending':
            task.status = 'working'
        elif task.status == 'working':
            task.status = 'done'
        else:
            task.status = 'pending'
        db.session.commit()
    else:
        flash('Task not found.', 'danger')

    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route('/clear', methods=['POST']) 
def clear_task():
    # require login
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    Task.query.delete()  # deletes all rows
    db.session.commit()
    flash('All tasks cleared!', 'info')
    return redirect(url_for('tasks.view_tasks'))
# from flask import Blueprint,render_template,request ,redirect ,url_for , flash , session 
# from app import db
# from app.models import Task 

# tasks_bp= Blueprint('tasks',__name__)# blueprint for tasks

# @tasks_bp.route('/tasks', methods=['GET'])
# def view_tasks():
#     if 'user' not in session:
#         flash('Please log in to view your tasks.', 'warning')
#         return redirect(url_for('auth.login'))
#     tasks = Task.query.order_by(Task.id.desc()).all()
#     return render_template('tasks.html', tasks==tasks)
# # @tasks_bp.route("/")
# # def view_tasks():
# #     if 'user' not in session:
# #         return render_template('login.html')
# #     tasks= Task.query.all()
# #     return render_template('task.html',tasks=tasks)
# @tasks_bp.route("/add",methods=['POST'])
# def add_task():
#     if 'user' not in session:
#         return redirect(url_for("auth.login"))
    
#     title=request.form.get('title')
#     if title:
#         new_task= Task(title==title, status='pending')
#         db.session.add(new_task)
#         db.session.commit()
#         flash(' task added succesfully..!!', "success")
#     return redirect(url_for('tasks.view_tasks')) 
# @tasks_bp.route('/toggle/<int:task_id>', methods=['POST'])
# def toggle_status(task_id):
#     task=Task.query.get(task_id)
#     if task:
#         if task.status=='pending':
#             task.status='working'
#         elif task.status=='working':
#             task.status='done'
#         else:
#             task.status='pending'
#         db.session.commit()
#     return redirect(url_for('tasks.view_tasks'))
# @tasks_bp.route("/clear",methods=['POST']) 
# def clear_task():
#     Task.query.delete()
#     db.session.commit()
#     flash('All the task are cleared!! ','info')
#     return redirect(url_for('tasks.view_tasks'))                 
