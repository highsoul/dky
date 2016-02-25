from zoo.extensions import db
from zoo.mmrelation.mm_relations import groups_admin, groups_members
from zoo.configs.default import DefaultConfig

import os, datetime, random


class Group(db.Model):

    __tablename__ = "groups"

    id = db.Column(db.Integer(), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.now(), nullable=True)

    private = db.Column(db.Boolean, default=False, nullable=False)

    name = db.Column(db.String(40), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    logo = db.Column(db.String(200), nullable=False)
    #banner = db.Column(db.String(200), nullable=False)
    set_logo = db.Column(db.Boolean, default=False, nullable=False)


    creator_id = db.Column(db.Integer, db.ForeignKey("users.id",ondelete="SET NULL"), nullable=False)
    members = db.relationship("User", secondary=groups_members, backref=db.backref("groups", lazy='dynamic'), lazy='dynamic')
    admins = db.relationship("User", secondary=groups_admin, backref=db.backref("admin_groups", lazy='dynamic'), lazy='joined')



    """ 设置随机小组图标 """
    def set_logo_auto(self):
        files = [x for x in os.listdir(DefaultConfig.LOCAL_GROUPLOGO_DIR)]
        self.logo = random.choice(files)

    """ 创建小组 """
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    """用户小组"""


    """ 序列化 """
    @property
    def serialize(self):
        return {
            'id': self.id,
            'private': self.private,
            'name': self.name
        }