from flask_login import UserMixin
from extensions import db, login_manager
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

CATEGORIES = ['Программное обеспечение', 'Оборудование', 'Сеть', 'Доступ', 'Другое']
PRIORITIES = ['Низкий', 'Средний', 'Высокий', 'Критический']
STATUSES = ['Новая', 'В работе', 'Ожидание', 'Решена', 'Закрыта']

MSK = ZoneInfo("Europe/Moscow")

def now_msk():
    return datetime.now(MSK).replace(tzinfo=None)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')
    is_approved = db.Column(db.Boolean, default=False)

    authored_tickets = db.relationship(
        'Ticket',
        foreign_keys='Ticket.author_id',
        backref='author',
        lazy=True
    )

    assigned_tickets = db.relationship(
        'Ticket',
        foreign_keys='Ticket.assigned_to_id',
        backref='assignee',
        lazy=True
    )

    comments = db.relationship('Comment', backref='user', lazy=True)

    @property
    def is_active(self):
        return self.is_approved


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class SLA(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    priority = db.Column(db.String(50), nullable=False)
    response_hours = db.Column(db.Integer, nullable=False, default=1)
    resolution_hours = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    description = db.Column(db.Text)

    tickets = db.relationship('Ticket', backref='sla', lazy=True)

    def __repr__(self):
        return f'<SLA {self.name}>'


class TicketHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
    field = db.Column(db.String(50), nullable=False)
    old_value = db.Column(db.String(100))
    new_value = db.Column(db.String(100))
    changed_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=now_msk)

    ticket = db.relationship('Ticket', backref='history')
    user = db.relationship('User')


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default='Новая')
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=now_msk)
    resolved_at = db.Column(db.DateTime, nullable=True)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    sla_id = db.Column(db.Integer, db.ForeignKey('sla.id'), nullable=True)

    comments = db.relationship(
        'Comment',
        backref='ticket',
        lazy=True,
        cascade='all, delete-orphan'
    )

    @property
    def resolution_deadline(self):
        if not self.created_at or not self.sla:
            return None
        return self.created_at + timedelta(hours=self.sla.resolution_hours)

    @property
    def is_resolved(self):
        return self.status in ['Решена', 'Закрыта']

    @property
    def is_overdue(self):
        deadline = self.resolution_deadline
        if not deadline:
            return False

        if self.resolved_at:
            return self.resolved_at > deadline

        return now_msk() > deadline and not self.is_resolved

    @property
    def sla_status(self):
        if not self.sla:
            return 'Не назначено'
        if self.is_overdue:
            return 'Просрочено'
        if self.is_resolved:
            return 'Выполнено в срок'
        return 'В работе'

    @property
    def time_left_text(self):
        deadline = self.resolution_deadline
        if not deadline:
            return 'SLA не назначено'

        if self.is_resolved:
            return 'Заявка закрыта'

        delta = deadline - now_msk()
        total_seconds = int(delta.total_seconds())

        if total_seconds <= 0:
            return 'Срок истёк'

        days, remainder = divmod(total_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, _ = divmod(remainder, 60)

        parts = []
        if days > 0:
            parts.append(f'{days} д')
        if hours > 0:
            parts.append(f'{hours} ч')
        if minutes > 0:
            parts.append(f'{minutes} мин')

        return ' '.join(parts) if parts else 'меньше минуты'

    @property
    def sla_state(self):
        if not self.sla:
            return 'Не назначено'

        if self.is_resolved:
            return 'Закрыта с нарушением' if self.is_overdue else 'Закрыта в срок'

        if self.is_overdue:
            return 'Просрочена'

        deadline = self.resolution_deadline
        if deadline:
            delta_hours = (deadline - now_msk()).total_seconds() / 3600
            if delta_hours <= 2:
                return 'На грани SLA'

        return 'В срок'


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=now_msk)

    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
