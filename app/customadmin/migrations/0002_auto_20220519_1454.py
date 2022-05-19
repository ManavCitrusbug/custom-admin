# Generated by Django 3.2.10 on 2022-05-19 14:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('customadmin', '0001_initial copy'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookedService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date when created.', null=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date when updated.', null=True, verbose_name='Updated At')),
                ('booking_charge', models.FloatField(blank=True, default=50, null=True)),
                ('service_date', models.DateField(blank=True, null=True)),
                ('service_time', models.TimeField(blank=True, null=True)),
                ('service_type', models.CharField(blank=True, choices=[('Local', 'Local'), ('Overseas', 'Overseas')], default='', max_length=100, null=True)),
            ],
            options={
                'verbose_name': 'Booked Service',
                'verbose_name_plural': 'Booked Services',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='CategoryImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date when created.', null=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date when updated.', null=True, verbose_name='Updated At')),
                ('category_image', models.ImageField(blank=True, null=True, upload_to='categories')),
            ],
            options={
                'verbose_name': 'CategoryImage',
                'verbose_name_plural': 'Category Images',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='FamilyCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date when created.', null=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date when updated.', null=True, verbose_name='Updated At')),
                ('code', models.CharField(blank=True, max_length=4, null=True)),
                ('meaning', models.TextField(blank=True, default='', max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Family Code',
                'verbose_name_plural': 'Family Codes',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='FoundationCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date when created.', null=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date when updated.', null=True, verbose_name='Updated At')),
                ('code', models.CharField(blank=True, max_length=4, null=True)),
                ('meaning', models.TextField(blank=True, default='', max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Foundation Code',
                'verbose_name_plural': 'Foundation Codes',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Inquiry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date when created.', null=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date when updated.', null=True, verbose_name='Updated At')),
                ('name', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.CharField(blank=True, default='', max_length=15, null=True)),
                ('note', models.CharField(blank=True, default='', max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Inquiry',
                'verbose_name_plural': 'Inquiries',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='InquiryType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date when created.', null=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date when updated.', null=True, verbose_name='Updated At')),
                ('inquiry_type', models.CharField(blank=True, default='', max_length=200, null=True)),
            ],
            options={
                'verbose_name': 'Inquiry Type',
                'verbose_name_plural': 'Inquiry Types',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='NumberCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date when created.', null=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date when updated.', null=True, verbose_name='Updated At')),
                ('code', models.CharField(blank=True, max_length=1, null=True)),
                ('meaning', models.TextField(blank=True, default='', max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Number Code',
                'verbose_name_plural': 'Number Codes',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='OtherCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date when created.', null=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date when updated.', null=True, verbose_name='Updated At')),
                ('code', models.CharField(blank=True, max_length=4, null=True)),
                ('meaning', models.TextField(blank=True, default='', max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Other Code',
                'verbose_name_plural': 'Other Codes',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='PersonalChart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date when created.', null=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date when updated.', null=True, verbose_name='Updated At')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('date_of_birth', models.DateField(blank=True, default='', null=True)),
            ],
            options={
                'verbose_name': 'Personal chart Detail',
                'verbose_name_plural': 'Personal chart Detail',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='PhoneNumberCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date when created.', null=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date when updated.', null=True, verbose_name='Updated At')),
                ('code', models.CharField(blank=True, max_length=2, null=True, unique=True)),
                ('code_text', models.TextField(blank=True, default='', null=True)),
            ],
            options={
                'verbose_name': 'Phone Number Code',
                'verbose_name_plural': 'Phone Number Codes',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ProductCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date when created.', null=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date when updated.', null=True, verbose_name='Updated At')),
                ('quantity', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Product Cart',
                'verbose_name_plural': 'Product Cart',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='PurchasedProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date when created.', null=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date when updated.', null=True, verbose_name='Updated At')),
                ('product_price', models.FloatField(blank=True, null=True)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('total_amount', models.FloatField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Purchased Product',
                'verbose_name_plural': 'Purchased Products',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date when created.', null=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date when updated.', null=True, verbose_name='Updated At')),
                ('service_image', models.ImageField(blank=True, null=True, upload_to='services', verbose_name='Service images')),
                ('name', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('booking_charge', models.FloatField(blank=True, default=50, null=True)),
                ('detail', models.TextField(blank=True, default='', max_length=255, null=True)),
                ('service_charge', models.FloatField(blank=True, null=True)),
                ('related_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_service', to='customadmin.service')),
            ],
            options={
                'verbose_name': 'Service',
                'verbose_name_plural': 'Services',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ServiceCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date when created.', null=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date when updated.', null=True, verbose_name='Updated At')),
                ('service_date', models.DateField(blank=True, null=True)),
                ('service_time', models.TimeField(blank=True, null=True)),
                ('service_type', models.CharField(blank=True, choices=[('Local', 'Local'), ('Overseas', 'Overseas')], default='', max_length=100, null=True)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customadmin.service')),
            ],
            options={
                'verbose_name': 'Service Cart',
                'verbose_name_plural': 'Service Cart',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ServiceCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date when created.', null=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date when updated.', null=True, verbose_name='Updated At')),
                ('category_name', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('category_description', models.TextField(blank=True, null=True)),
                ('method_description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Service Category',
                'verbose_name_plural': 'Service Categories',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ShopProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date when created.', null=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date when updated.', null=True, verbose_name='Updated At')),
                ('product_image', models.ImageField(blank=True, null=True, upload_to='products', verbose_name='Product images')),
                ('name', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
                ('detail', models.TextField(blank=True, default='', max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Shop Product',
                'verbose_name_plural': 'Shop Products',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='SocialCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date when created.', null=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date when updated.', null=True, verbose_name='Updated At')),
                ('code', models.CharField(blank=True, max_length=4, null=True)),
                ('meaning', models.TextField(blank=True, default='', max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Social Code',
                'verbose_name_plural': 'Social Codes',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date when created.', null=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date when updated.', null=True, verbose_name='Updated At')),
                ('time_slot', models.TimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Time Slot',
                'verbose_name_plural': 'Time Slots',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='TransactionDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date when created.', null=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date when updated.', null=True, verbose_name='Updated At')),
                ('transaction_id', models.UUIDField(blank=True, default=uuid.uuid4, null=True)),
                ('card_id', models.CharField(blank=True, max_length=255, verbose_name='Card Id')),
                ('customer_id', models.CharField(blank=True, max_length=255, verbose_name='Customer Id')),
                ('charge_id', models.CharField(blank=True, max_length=255, verbose_name='Charge Id')),
                ('charge_object', models.CharField(blank=True, max_length=255, null=True, verbose_name='Object')),
                ('amount', models.CharField(blank=True, max_length=255, null=True, verbose_name='Amount')),
                ('amount_refunded', models.CharField(blank=True, max_length=255, null=True, verbose_name='Amount refunded')),
                ('application', models.CharField(blank=True, max_length=255, null=True, verbose_name='Application')),
                ('application_fee', models.CharField(blank=True, max_length=255, null=True, verbose_name='Application fee')),
                ('application_fee_amount', models.CharField(blank=True, max_length=255, null=True, verbose_name='Application fee amount')),
                ('balance_transaction', models.CharField(blank=True, max_length=255, verbose_name='Balance transaction')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Address')),
                ('email', models.CharField(blank=True, max_length=255, null=True, verbose_name='Email')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Name')),
                ('phone', models.CharField(blank=True, max_length=255, null=True, verbose_name='Phone')),
                ('calculated_statement_descriptor', models.CharField(blank=True, max_length=255, null=True, verbose_name='Calculated statement descriptor')),
                ('captured', models.BooleanField()),
                ('created', models.CharField(blank=True, max_length=255, null=True, verbose_name='Created')),
                ('currency', models.CharField(blank=True, max_length=255, null=True, verbose_name='Currency')),
                ('customer', models.CharField(blank=True, max_length=255, null=True, verbose_name='Customer')),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Description')),
                ('disputed', models.BooleanField()),
                ('failure_code', models.CharField(blank=True, max_length=255, null=True, verbose_name='Failure code')),
                ('failure_message', models.CharField(blank=True, max_length=255, null=True, verbose_name='Failure message')),
                ('fraud_details', models.CharField(blank=True, max_length=255, null=True, verbose_name='Fraud details')),
                ('invoice', models.CharField(blank=True, max_length=255, null=True, verbose_name='Invoice')),
                ('livemode', models.BooleanField()),
                ('metadata', models.CharField(blank=True, max_length=255, null=True, verbose_name='Metadata')),
                ('on_behalf_of', models.CharField(blank=True, max_length=255, null=True, verbose_name='On behalf of')),
                ('order', models.CharField(blank=True, max_length=255, null=True, verbose_name='Order')),
                ('outcome', models.CharField(blank=True, max_length=255, null=True, verbose_name='Outcome')),
                ('paid', models.BooleanField()),
                ('payment_intent', models.CharField(blank=True, max_length=255, null=True, verbose_name='Payment intent')),
                ('payment_method', models.CharField(blank=True, max_length=255, verbose_name='Card Id')),
                ('brand', models.CharField(blank=True, max_length=255, null=True, verbose_name='Brand')),
                ('address_line1_check', models.CharField(blank=True, max_length=255, null=True, verbose_name='Address line1 check')),
                ('address_postal_code_check', models.CharField(blank=True, max_length=255, null=True, verbose_name='Address postal code check')),
                ('cvc_check', models.CharField(blank=True, max_length=255, null=True, verbose_name='CVC check')),
                ('country', models.CharField(blank=True, max_length=255, null=True, verbose_name='Country')),
                ('exp_month', models.CharField(blank=True, max_length=255, null=True, verbose_name='Exp month')),
                ('exp_year', models.CharField(blank=True, max_length=255, null=True, verbose_name='Exp year')),
                ('fingerprint', models.CharField(blank=True, max_length=255, null=True, verbose_name='Fingerprint')),
                ('funding', models.CharField(blank=True, max_length=255, null=True, verbose_name='Funding')),
                ('installments', models.CharField(blank=True, max_length=255, null=True, verbose_name='Installments')),
                ('last4', models.CharField(blank=True, max_length=255, null=True, verbose_name='Last4 digit')),
                ('network', models.CharField(blank=True, max_length=255, null=True, verbose_name='Network')),
                ('three_d_secure', models.CharField(blank=True, max_length=255, null=True, verbose_name='3D secure')),
                ('wallet', models.CharField(blank=True, max_length=255, null=True, verbose_name='Wallet')),
                ('charge_type', models.CharField(blank=True, max_length=255, null=True, verbose_name='Type')),
                ('receipt_email', models.CharField(blank=True, max_length=255, null=True, verbose_name='Receipt email')),
                ('receipt_number', models.CharField(blank=True, max_length=255, null=True, verbose_name='Receipt number')),
                ('receipt_url', models.CharField(blank=True, max_length=255, null=True, verbose_name='Receipt URL')),
                ('refunded', models.BooleanField()),
                ('refunds_object', models.CharField(blank=True, max_length=255, null=True, verbose_name='Refunds object')),
                ('refunds_data', models.CharField(blank=True, max_length=255, null=True, verbose_name='Refunds data')),
                ('refunds_has_more', models.BooleanField()),
                ('refunds_url', models.CharField(blank=True, max_length=255, null=True, verbose_name='Refunds URL')),
                ('review', models.CharField(blank=True, max_length=255, null=True, verbose_name='Review')),
                ('shipping', models.CharField(blank=True, max_length=255, null=True, verbose_name='Shipping')),
                ('source_transfer', models.CharField(blank=True, max_length=255, null=True, verbose_name='Source transfer')),
                ('statement_descriptor', models.CharField(blank=True, max_length=255, null=True, verbose_name='Statement descriptor')),
                ('statement_descriptor_suffix', models.CharField(blank=True, max_length=255, null=True, verbose_name='Statement descriptor suffix')),
                ('status', models.CharField(blank=True, max_length=255, null=True, verbose_name='Status')),
                ('transfer_data', models.CharField(blank=True, max_length=255, null=True, verbose_name='Transfer data')),
                ('transfer_group', models.CharField(blank=True, max_length=255, null=True, verbose_name='Transfer group')),
                ('source', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Source')),
            ],
            options={
                'verbose_name': 'Transaction Detail',
                'verbose_name_plural': 'Transaction Details',
            },
        ),
        migrations.CreateModel(
            name='UserPhoneNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date when created.', null=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date when updated.', null=True, verbose_name='Updated At')),
                ('phone', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'verbose_name': 'User Phone Numer',
                'verbose_name_plural': 'User Phone Numers',
                'ordering': ['-created_at'],
            },
        ),
        migrations.RenameField(
            model_name='testimonial',
            old_name='designition',
            new_name='designation',
        ),
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='device',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='email_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='otp',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='otp_expired_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='password_reset_link',
            field=models.UUIDField(blank=True, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, default='../static/assets/images/profile.jpg', null=True, upload_to='profile_image', verbose_name='Profile Image'),
        ),
        migrations.DeleteModel(
            name='Enquiry',
        ),
        migrations.DeleteModel(
            name='EnquiryType',
        ),
        migrations.AddField(
            model_name='transactiondetail',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='servicecart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='service',
            name='service_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customadmin.servicecategory'),
        ),
        migrations.AddField(
            model_name='purchasedproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customadmin.shopproduct'),
        ),
        migrations.AddField(
            model_name='purchasedproduct',
            name='transaction_detail',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customadmin.transactiondetail'),
        ),
        migrations.AddField(
            model_name='purchasedproduct',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='productcart',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customadmin.shopproduct'),
        ),
        migrations.AddField(
            model_name='productcart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='inquiry',
            name='inquiry_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customadmin.inquirytype'),
        ),
        migrations.AddField(
            model_name='categoryimage',
            name='service_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customadmin.servicecategory'),
        ),
        migrations.AddField(
            model_name='bookedservice',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customadmin.service'),
        ),
        migrations.AddField(
            model_name='bookedservice',
            name='transaction_detail',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customadmin.transactiondetail'),
        ),
        migrations.AddField(
            model_name='bookedservice',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]