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
    listened = db.BooleanField(default=False)

    def __unicode__(self):
        return self.callSid

    def format_seconds(self, seconds):
        """ string formated duration in minutes and seconds """
        return '%s:%s' % (int(seconds/60), seconds%60,)

    def format_duration(self):
        if self.duration:
            return self.format_seconds(self.duration)
        else:
            return 'unknown'

    def format_recording_duraton(self):
        if self.recordingDuration:
            return self.format_seconds(self.recordingDuration)
        else:
            return 'unknown'
