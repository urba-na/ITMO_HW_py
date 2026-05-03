from datetime import datetime

from flask import render_template, request, redirect, url_for, abort, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import aliased
from functools import wraps

from config import DEFAULT_USER_PASSWORD, DEFAULT_ADMIN_USERNAME
from extensions import db
from models import User, Ticket, Comment, TicketHistory, SLA, CATEGORIES, PRIORITIES, STATUSES


def role_required(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('login'))
            if current_user.role not in roles:
                abort(403)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def init_routes(app):

    @app.route('/')
    def home():
        return redirect(url_for('login'))

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username'].strip()
            email = request.form['email'].strip().lower()
            password = request.form['password']

            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                flash('Пользователь с таким логином уже существует.', 'warning')
                return redirect(url_for('register'))

            existing_email = User.query.filter_by(email=email).first()
            if existing_email:
                flash('Пользователь с такой электронной почтой уже существует.', 'warning')
                return redirect(url_for('register'))

            hashed_password = generate_password_hash(password)
            user = User(
                username=username,
                email=email,
                password=hashed_password,
                role='user',
                is_approved=False
            )

            db.session.add(user)
            db.session.commit()

            flash('Регистрация отправлена. Ожидайте подтверждения администратором.', 'success')
            return redirect(url_for('login'))

        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        message = None

        if request.method == 'POST':
            username = request.form['username'].strip()
            password = request.form['password']

            user = User.query.filter_by(username=username).first()

            if not user:
                message = 'Пользователь не найден'
            elif not check_password_hash(user.password, password):
                message = 'Неверный пароль'
            elif not user.is_approved:
                message = 'Ваша регистрация ещё не подтверждена администратором'
            else:
                login_user(user)
                return redirect(url_for('dashboard'))

        return render_template('login.html', message=message)

    @app.route('/dashboard')
    @login_required
    def dashboard():
        author_alias = aliased(User)
        assignee_alias = aliased(User)

        query = Ticket.query \
            .outerjoin(author_alias, Ticket.author_id == author_alias.id) \
            .outerjoin(assignee_alias, Ticket.assigned_to_id == assignee_alias.id)

        if current_user.role == 'user':
            query = query.filter(Ticket.author_id == current_user.id)

        ticket_id = request.args.get('ticket_id', '').strip()
        title = request.args.get('title', '').strip()
        category = request.args.get('category', '').strip()
        priority = request.args.get('priority', '').strip()
        author = request.args.get('author', '').strip()
        assigned_to = request.args.get('assigned_to', '').strip()
        status = request.args.get('status', '').strip()
        created_at = request.args.get('created_at', '').strip()

        sort_by = request.args.get('sort_by', 'created_at').strip()
        sort_dir = request.args.get('sort_dir', 'desc').strip()

        if ticket_id and ticket_id.isdigit():
            query = query.filter(Ticket.id == int(ticket_id))

        if title:
            query = query.filter(Ticket.title.ilike(f'%{title}%'))

        if category:
            query = query.filter(Ticket.category == category)

        if priority:
            query = query.filter(Ticket.priority == priority)

        if author:
            query = query.filter(author_alias.username.ilike(f'%{author}%'))

        if assigned_to:
            query = query.filter(assignee_alias.username.ilike(f'%{assigned_to}%'))

        if status:
            query = query.filter(Ticket.status == status)

        if created_at:
            query = query.filter(Ticket.created_at.cast(db.String).ilike(f'%{created_at}%'))

        sort_columns = {
            'id': Ticket.id,
            'created_at': Ticket.created_at,
            'title': Ticket.title,
            'status': Ticket.status,
            'priority': Ticket.priority,
            'category': Ticket.category,
        }

        sort_column = sort_columns.get(sort_by, Ticket.created_at)

        if sort_dir == 'asc':
            query = query.order_by(sort_column.asc())
        else:
            query = query.order_by(sort_column.desc())

        tickets = query.all()

        return render_template(
            'dashboard.html',
            tickets=tickets,
            user=current_user,
            CATEGORIES=CATEGORIES,
            PRIORITIES=PRIORITIES,
            STATUSES=STATUSES,
            sort_by=sort_by,
            sort_dir=sort_dir
        )

    @app.route('/tickets/create', methods=['GET', 'POST'])
    @login_required
    def create_ticket():
        if request.method == 'POST':
            title = request.form['title'].strip()
            description = request.form['description'].strip()
            category = request.form['category']
            priority = request.form['priority']

            sla = SLA.query.filter_by(priority=priority, is_active=True) \
                .order_by(SLA.resolution_hours.asc()) \
                .first()

            ticket = Ticket(
                title=title,
                description=description,
                category=category,
                priority=priority,
                status='Новая',
                author_id=current_user.id,
                sla_id=sla.id if sla else None
            )

            db.session.add(ticket)
            db.session.flush()

            db.session.add(TicketHistory(
                ticket_id=ticket.id,
                field='create',
                old_value='',
                new_value='Заявка создана',
                changed_by_id=current_user.id
            ))

            if sla:
                db.session.add(TicketHistory(
                    ticket_id=ticket.id,
                    field='sla',
                    old_value='',
                    new_value=sla.name,
                    changed_by_id=current_user.id
                ))

            db.session.commit()

            flash('Заявка создана.', 'success')
            return redirect(url_for('dashboard'))

        return render_template(
            'create_ticket.html',
            CATEGORIES=CATEGORIES,
            PRIORITIES=PRIORITIES
        )

    @app.route('/tickets/<int:ticket_id>', methods=['GET', 'POST'])
    @login_required
    def ticket_detail(ticket_id):
        ticket = Ticket.query.get_or_404(ticket_id)

        if current_user.role == 'user' and ticket.author_id != current_user.id:
            flash('У вас нет доступа к этой заявке.', 'danger')
            return redirect(url_for('dashboard'))

        comments = Comment.query.filter_by(ticket_id=ticket.id).order_by(Comment.created_at.asc()).all()
        history = TicketHistory.query.filter_by(ticket_id=ticket.id).order_by(TicketHistory.created_at.desc()).all()
        eligible_users = User.query.filter(User.role.in_(['engineer', 'admin'])).order_by(User.username.asc()).all()

        if request.method == 'POST':
            action = request.form.get('action')

            if action == 'add_comment':
                content = request.form.get('content', '').strip()

                if content:
                    comment = Comment(
                        text=content,
                        ticket_id=ticket.id,
                        user_id=current_user.id
                    )
                    db.session.add(comment)
                    db.session.commit()
                    flash('Комментарий добавлен.', 'success')
                else:
                    flash('Комментарий не может быть пустым.', 'warning')

                return redirect(url_for('ticket_detail', ticket_id=ticket.id))

            elif action == 'update_ticket':
                if current_user.role not in ['admin', 'engineer']:
                    flash('У вас нет прав для управления заявкой.', 'danger')
                    return redirect(url_for('ticket_detail', ticket_id=ticket.id))

                old_status = ticket.status
                old_assigned_to_id = ticket.assigned_to_id

                new_status = request.form.get('status')
                assigned_to_id = request.form.get('assigned_to_id')

                if new_status and new_status != ticket.status:
                    ticket.status = new_status

                    db.session.add(TicketHistory(
                        ticket_id=ticket.id,
                        field='status',
                        old_value=old_status or '',
                        new_value=new_status,
                        changed_by_id=current_user.id
                    ))

                if assigned_to_id:
                    new_assigned_to_id = int(assigned_to_id)
                else:
                    new_assigned_to_id = None

                if old_assigned_to_id != new_assigned_to_id:
                    old_assignee = User.query.get(old_assigned_to_id) if old_assigned_to_id else None
                    new_assignee = User.query.get(new_assigned_to_id) if new_assigned_to_id else None

                    ticket.assigned_to_id = new_assigned_to_id

                    db.session.add(TicketHistory(
                        ticket_id=ticket.id,
                        field='assigned_to',
                        old_value=old_assignee.username if old_assignee else '',
                        new_value=new_assignee.username if new_assignee else '',
                        changed_by_id=current_user.id
                    ))

                if ticket.status in ['Решена', 'Закрыта']:
                    if not ticket.resolved_at:
                        ticket.resolved_at = datetime.utcnow()
                else:
                    ticket.resolved_at = None

                db.session.commit()
                flash('Заявка обновлена.', 'success')
                return redirect(url_for('ticket_detail', ticket_id=ticket.id))

        return render_template(
            'ticket_detail.html',
            ticket=ticket,
            comments=comments,
            history=history,
            eligible_users=eligible_users,
            STATUSES=STATUSES
        )

    @app.route('/users', methods=['GET', 'POST'])
    @login_required
    @role_required('admin')
    def users_list():
        if request.method == 'POST':
            action = request.form.get('action')
            user_id = request.form.get('user_id')
            user_obj = User.query.get_or_404(user_id)

            if action == 'update_role':
                role = request.form.get('role')

                if user_obj.username == DEFAULT_ADMIN_USERNAME:
                    flash('Нельзя изменить роль встроенного администратора.', 'warning')
                else:
                    user_obj.role = role
                    db.session.commit()
                    flash(f'Роль пользователя {user_obj.username} изменена.', 'success')

                return redirect(url_for('users_list'))

            elif action == 'update_approval':
                requested_value = 'is_approved' in request.form

                if user_obj.username == DEFAULT_ADMIN_USERNAME and not requested_value:
                    flash('Нельзя отключить доступ встроенному администратору.', 'warning')
                else:
                    user_obj.is_approved = requested_value
                    db.session.commit()

                    if requested_value:
                        flash(f'Доступ пользователю {user_obj.username} разрешён.', 'success')
                    else:
                        flash(f'Доступ пользователю {user_obj.username} отключён.', 'warning')

                return redirect(url_for('users_list'))

            elif action == 'reset_password':
                if user_obj.username == DEFAULT_ADMIN_USERNAME:
                    flash('Сброс пароля встроенного администратора через интерфейс запрещён.', 'warning')
                else:
                    user_obj.password = generate_password_hash(DEFAULT_USER_PASSWORD)
                    db.session.commit()
                    flash(f'Пароль пользователя {user_obj.username} сброшен на пароль по умолчанию.', 'info')

                return redirect(url_for('users_list'))

        users = User.query.order_by(User.id.asc()).all()
        return render_template('users.html', users=users)

    @app.route('/sla', methods=['GET', 'POST'])
    @login_required
    @role_required('admin')
    def sla_list():
        if request.method == 'POST':
            action = request.form.get('action')

            if action == 'create':
                sla = SLA(
                    name=request.form.get('name', '').strip(),
                    priority=request.form.get('priority'),
                    response_hours=int(request.form.get('response_hours', 1)),
                    resolution_hours=int(request.form.get('resolution_hours', 24)),
                    is_active='is_active' in request.form,
                    description=request.form.get('description', '').strip()
                )
                db.session.add(sla)
                db.session.commit()
                flash('SLA-правило создано.', 'success')
                return redirect(url_for('sla_list'))

            elif action == 'update':
                sla_id = request.form.get('sla_id')
                sla = SLA.query.get_or_404(sla_id)

                sla.name = request.form.get('name', '').strip()
                sla.priority = request.form.get('priority')
                sla.response_hours = int(request.form.get('response_hours', 1))
                sla.resolution_hours = int(request.form.get('resolution_hours', 24))
                sla.is_active = 'is_active' in request.form
                sla.description = request.form.get('description', '').strip()

                db.session.commit()
                flash('SLA-правило обновлено.', 'success')
                return redirect(url_for('sla_list'))

            elif action == 'delete':
                sla_id = request.form.get('sla_id')
                sla = SLA.query.get_or_404(sla_id)

                if sla.tickets:
                    flash('Нельзя удалить SLA, которое уже назначено заявкам.', 'danger')
                    return redirect(url_for('sla_list'))

                db.session.delete(sla)
                db.session.commit()
                flash('SLA-правило удалено.', 'success')
                return redirect(url_for('sla_list'))

        slas = SLA.query.order_by(SLA.id.asc()).all()
        return render_template('sla.html', slas=slas, PRIORITIES=PRIORITIES)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))
