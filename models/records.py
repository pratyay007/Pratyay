from datetime import datetime
from pytz import timezone
from config import db


# class UserCreation(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     creation_time = db.Column(db.DateTime, default=datetime.utcnow)
#     created_by = db.Column(db.String(255), nullable=False)

#     def __init__(self, created_by):
#         self.created_by = created_by



class TrnApprovalTask(db.Model):
    __tablename__ = 'trn_approval_task'

    tat_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tat_task_type = db.Column(db.String(20))
    tat_task_state = db.Column(db.String(20))
    tat_reason = db.Column(db.String(200))
    tat_requested_id = db.Column(db.String(50))
    tat_request_by = db.Column(db.String(50))
    tat_approver = db.Column(db.String(50))
    tat_resource_group = db.Column(db.String(250))
    tat_time = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone('Asia/Kolkata')).replace(microsecond=0))

