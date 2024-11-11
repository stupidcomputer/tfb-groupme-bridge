from django.db import models
import uuid

def get_uuid():
    return uuid.uuid4().hex

class Organization(models.Model):
    name = models.CharField(
        max_length=256,
    )
    _sender_url = models.CharField(
        max_length=256,
        default = get_uuid
    )
    _receiver_url = models.CharField(
        max_length=256,
        default = get_uuid
    )

    @property
    def add_sending_group(self):
        return "https://tfb.beepboop.systems/groupme/add/send/{}".format(
            self._sender_url
        )
    @property
    def add_receiving_group(self):
        return "https://tfb.beepboop.systems/groupme/add/recv/{}".format(
            self._receiver_url
        )
    
class Group(models.Model):
    name = models.CharField(max_length=256)
    group_id = models.CharField(max_length=256)
    bot_id = models.CharField(max_length=256)
    can_send_notices = models.BooleanField()
    belongs_to = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)