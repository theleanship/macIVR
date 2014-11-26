from ivr import db
from datetime import datetime


class Call(db.Document):
    created_at = db.DateTimeField(default=datetime.now, required=True)
    callSid = db.StringField(max_length=255, required=True)
    fromNumber = db.StringField(max_length=255, required=False)
    toNumber = db.StringField(max_length=255)
    duration = db.IntField()
    recordingUrl = db.StringField(max_length=255)
    recordingSid = db.StringField(max_length=255)
    recordingDuration = db.IntField()

    def __unicode__(self):
        return self.callSid