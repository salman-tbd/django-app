import datetime
import random
from django.db import models

# Create your models here.
from django.utils import timezone
from django.core.exceptions import ValidationError

from django.db.models import Q

priority_choice = [
    ('Highest', 'Highest'),
    ('High', 'High'),
    ('Medium', 'Medium'),
    ('Low', 'Low'),
    ('Lowest', 'Lowest'),
]

source = [
    ('', '-Select'),
    ('Lead', 'Lead'),
    ('Customer', 'Customer'),
    ('Employee', 'Employee'),
    ('Other', 'Other'),
]

status = [
    ('', '-Select'),
    ('All', 'All'),
    ('Active', 'Active'),
    ('In-Progress', 'In-Progress'),
    ('Completed', 'Completed'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
]

status_choices = [
    ('Approve', 'Approve'),
    ('Pending', 'Pending'),
    ('Rejected', 'Rejected'),
]

recurring_type = [
    ('Daily', 'Daily'),
    ('Monthly', 'Monthly'),
    ('Yearly', 'Yearly'),
    ('Weekly', 'Weekly'),
    ('custom', 'custom'),
]
class Tbl_FieldTask_Purpose_Master(models.Model):
    fieldtask_purpose_master_id = models.AutoField(primary_key=True)
    purpose = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return str(self.fieldtask_purpose_master_id)

    def save(self, *args, **kwargs):
        super(Tbl_FieldTask_Purpose_Master, self).save(*args, **kwargs)
        self.process_data()

    def process_data(self):
        obj = Tbl_FieldTask_Purpose_Master.objects.filter(Q(salt='') | Q(salt=None))
        secrete_key = list(settings.AUTH_SEC_PAIRS[random.randint(0, 99)].values())[0]
        for a in obj:
            encrypted = ec.encrypt(str(a.fieldtask_purpose_master_id), secrete_key)
            Tbl_FieldTask_Purpose_Master.objects.filter(fieldtask_purpose_master_id=a.fieldtask_purpose_master_id).update(
                salt=encrypted['salt'], cipher_text=encrypted['cipher_text'], nonce=encrypted['nonce'],
                tag=encrypted['tag'])

class Tbl_FieldTask(models.Model):
    filedtask_id = models.AutoField(primary_key=True)
    fieldtask_purpose_master_id = models.ForeignKey(Tbl_FieldTask_Purpose_Master, on_delete=models.PROTECT, null=True, blank=True)
    start_destination = models.CharField(max_length=500, blank=True, null=True)
    end_destination = models.CharField(max_length=500, blank=True, null=True)
    total_km = models.CharField(max_length=500, blank=True, null=True)
    from_dest = models.CharField(max_length=500, blank=True, null=True)
    to_dest = models.CharField(max_length=500, blank=True, null=True)

    # start_longitude = models.CharField(max_length=500, blank=True, null=True) # after r&d in google
    # end_longitude = models.CharField(max_length=500, blank=True, null=True) # after r&d in google
    # route_recording = models.CharField(max_length=500, blank=True, null=True) # after r&d in google

    ''' many more filed to added after r&d in google'''

    def __str__(self):
        return str(self.filedtask_id)

    def save(self, *args, **kwargs):
        super(Tbl_FieldTask, self).save(*args, **kwargs)
        self.process_data()

    def process_data(self):
        obj = Tbl_FieldTask.objects.filter(Q(salt='') | Q(salt=None))
        secrete_key = list(settings.AUTH_SEC_PAIRS[random.randint(0, 99)].values())[0]
        for a in obj:
            encrypted = ec.encrypt(str(a.filedtask_id), secrete_key)
            Tbl_FieldTask.objects.filter(filedtask_id=a.filedtask_id).update(
                salt=encrypted['salt'], cipher_text=encrypted['cipher_text'], nonce=encrypted['nonce'],
                tag=encrypted['tag'])


class Tbl_TaskTemplate(models.Model):
    task_template_id = models.AutoField(primary_key=True)
    template_title = models.CharField(max_length=500, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    est_min = models.PositiveBigIntegerField(null=True, blank=True)
    template_status = models.CharField(choices=status_choices, max_length=50, null=True, blank=True, default="Pending")
    priority = models.CharField(max_length=30, choices=priority_choice, default="Medium", null=True, blank=True)
    is_fieldtask = models.BooleanField(default=False)
    show_for_all = models.BooleanField(default=False)
    def __str__(self):
        return str(self.template_title)

    def save(self, *args, **kwargs):
        super(Tbl_TaskTemplate, self).save(*args, **kwargs)
        self.process_data()

    def process_data(self):
        obj = Tbl_TaskTemplate.objects.filter(Q(salt='') | Q(salt=None))
        secrete_key = list(settings.AUTH_SEC_PAIRS[random.randint(0, 99)].values())[0]
        for a in obj:
            encrypted = ec.encrypt(str(a.task_template_id), secrete_key)
            Tbl_TaskTemplate.objects.filter(task_template_id=a.task_template_id).update(
                salt=encrypted['salt'], cipher_text=encrypted['cipher_text'], nonce=encrypted['nonce'],
                tag=encrypted['tag'])

class Tbl_Tasks(models.Model):
    tasks_id = models.AutoField(primary_key=True)
    task_title = models.CharField(max_length=500, blank=True, null=True)
    task_description = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=30, choices=priority_choice, default="Medium", null=True, blank=True)
    task_deadline = timezone.now() + timezone.timedelta(days=2)  # default is 2 days..
    deadline = models.DateTimeField(default=task_deadline)

    in_desktop_crm = models.BooleanField(default=False)

    # added by harsh
    est_min = models.PositiveBigIntegerField(null=True, blank=True)
    remind_before_min = models.PositiveBigIntegerField(null=True, blank=True, default=0)
    user_deadline = models.DateTimeField(null=True, blank=True)
    approval_deadline = models.DateTimeField(null=True, blank=True)
    source = models.CharField(max_length=100, choices=source, default='Other', blank=True, null=True)
    source_id = models.PositiveBigIntegerField(blank=True, null=True, default=0)  # Lead id, customer id, employee id
    doc_approval = models.BooleanField(default=False)
    status = models.CharField(max_length=100, choices=status, default='Active')
    rejected_note = models.CharField(max_length=500, blank=True, null=True)
    completed_date = models.DateTimeField(null=True, blank=True)

    start_date = models.DateTimeField(null=True, blank=True)

    otp = models.PositiveBigIntegerField(blank=True, null=True)
    otp_date = models.DateTimeField(null=True, blank=True)
    spend_min = models.PositiveBigIntegerField(null=True, blank=True)
    completed_percentage = models.PositiveBigIntegerField(blank=True, null=True, default=0)

    # additional field
    is_field_task = models.BooleanField(default=False)
    filedtask_id = models.ManyToManyField(Tbl_FieldTask, blank=True)
    task_template_id = models.ForeignKey(Tbl_TaskTemplate, on_delete=models.PROTECT, null=True, blank=True)
    is_recurring_task = models.BooleanField(default=False)
    recurring_type = models.CharField(max_length=100, choices=recurring_type, blank=True, null=True)
    # custom_recurring_id = models.ForeignKey(Tbl_custom_type_recurring, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return str(self.task_title)

    def save(self, *args, **kwargs):
        super(Tbl_Tasks, self).save(*args, **kwargs)
        self.process_data()

    def process_data(self):
        obj = Tbl_Tasks.objects.filter(Q(salt='') | Q(salt=None))
        secrete_key = list(settings.AUTH_SEC_PAIRS[random.randint(0, 99)].values())[0]
        for a in obj:
            encrypted = ec.encrypt(str(a.tasks_id), secrete_key)
            Tbl_Tasks.objects.filter(
                tasks_id=a.tasks_id).update(
                salt=encrypted['salt'], cipher_text=encrypted['cipher_text'], nonce=encrypted['nonce'],
                tag=encrypted['tag'])

class Tbl_Allowance_Master:
    allowance_id = models.AutoField(primary_key=True)
    allowance_name = models.CharField(max_length=500, blank=True, null=True)
    allowance_type = models.CharField(max_length=500, blank=True, null=True)
    allowance_amount = models.PositiveBigIntegerField(blank=True, null=True)
    status = models.BooleanField(default=True)
    with_effect_from = models.DateTimeField(null=True, blank=True)
    with_effect_to = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.allowance_id)

    def save(self, *args, **kwargs):
        super(Tbl_Allowance_Master, self).save(*args, **kwargs)
        self.process_data()

    def process_data(self):
        obj = Tbl_Allowance_Master.objects.filter(Q(salt='') | Q(salt=None))
        secrete_key = list(settings.AUTH_SEC_PAIRS[random.randint(0, 99)].values())[0]
        for a in obj:
            encrypted = ec.encrypt(str(a.allowance_id), secrete_key)
            Tbl_Allowance_Master.objects.filter(
                allowance_id=a.allowance_id).update(
                salt=encrypted['salt'], cipher_text=encrypted['cipher_text'], nonce=encrypted['nonce'],
                tag=encrypted['tag'])


class Tbl_System_Config(models.Model):
    system_config_id = models.AutoField(primary_key=True)

    #for task configuration
    create_task_after_min = models.BigIntegerField(blank=True, null=True)  # task will be create after this minutes
    task_deadline_min = models.BigIntegerField(blank=True, null=True)  # task deadline

    #for book_by reward
    reward_amount = models.BigIntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.system_config_id)

    def save(self, *args, **kwargs):
        super(Tbl_System_Config, self).save(*args, **kwargs)
        self.process_data()

    def process_data(self):
        obj = Tbl_System_Config.objects.filter(Q(salt='') | Q(salt=None))
        secrete_key = list(settings.AUTH_SEC_PAIRS[random.randint(0, 99)].values())[0]
        for a in obj:
            encrypted = ec.encrypt(str(a.system_config_id), secrete_key)
            Tbl_System_Config.objects.filter(
                system_config_id=a.system_config_id).update(
                salt=encrypted['salt'], cipher_text=encrypted['cipher_text'], nonce=encrypted['nonce'],
                tag=encrypted['tag'])
