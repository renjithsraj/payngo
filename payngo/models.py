from django.db import models
from django.conf import settings as d_set
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.utils.translation import gettext_lazy as _


PAYMENT_GATEWAYS = (
    ('PU', _('PAYU'))
)

TRANSACTION_STATUS = (
    ('SU', 'SUCCESS'),
    ('FA', 'FAILED'),
    ('CA', 'CANCEL'),
    ('PE', 'PENDING')
    )


class PayngoTimeStampModel(models.Model):
    created = models.DateTimeField(_('Created Date'), auto_now_add=True, auto_now=False, null=True, blank=True)
    updated = models.DateTimeField('Updated Date', auto_now=True, auto_now_add=False, null=True, blank=True)
    is_active = models.BooleanField('Active ?', default=False)
    
    class Meta:
        abstract = True


class PayngoGatewayConfiguration(models.Model):
    config_by = models.ForeignKey('Configured BY', d_set.AUTH_USER_MODEL, on_delete=models.CASCADE)
    payment_gateway = models.CharField('Payment Gateway', max_length=3, choices= PAYMENT_GATEWAYS)
    gateway_server = models.CharField(choices=(('DEMO', 'DE'), ('LIVE', 'LI')), max_length= 2)
    credentials = models.TextField('Credentials(please reffer doc)')
    percentage = models.IntegerField('Request Percentage', help_text='If you require mulipile payment gateway \
        in your application then provide the percentage', default=100)
    is_active = models.BooleanField('Active or Not', default=True,)
    
    def clean(self):
        if PayngoGatewayConfiguration.objects.filter(is_active=True, 
                                                     payment_gateway=self.payment_gateway).exists():
            raise ValidationError(_('The Selected gateway already in Active.'))
        if PayngoGatewayConfiguration.objects.filter(payment_gateway=self.payment_gateway,
                                                     gateway_server=self.gateway_server).exists():
            raise ValidationError({'gateway_server': ValidationError(
                    _('Selected server is already selected in the Payment gateway'))})
            
class PayangoTransaction(PayngoTimeStampModel):
    """Model definition for PayangoTransaction."""
    created_by = models.ForeignKey('Created BY', d_set.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                                   related_name='transactions')
    transaction_id = models.CharField('Transaction ID', max_length=200)
    transaction_amount = models.FloatField('amonut', editable=False)
    transaction_status = models.CharField('Transaction Status', max_length=3)
    requested_data = models.TextField('Requested Data')
    
    ### Payment Gateway related fields
    payment_gateway = models.ForeignKey(PayngoGatewayConfiguration, )
    txn_refference_id = models.CharField('Transaction Refferance ID', help_text='Refferance ID from Payment Gateways')
    

    class Meta:
        """Meta definition for PayangoTransaction."""

        verbose_name = 'PayangoTransaction'
        verbose_name_plural = 'PayangoTransactions'

    def __str__(self):
        """Unicode representation of PayangoTransaction."""
        pass
