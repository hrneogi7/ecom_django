from django.db import migrations
from api.user.models import CustomUser


class Migration(migrations.Migration):
    def seed_data(apps, schema_editor):
        user = CustomUser(name="hrithik",
                          email="hrneogi@gmail.com",
                          is_staff=True,
                          is_superuser=True,
                          phone="7687925467",
                          gender="Male"
                          )
        user.set_password("Xmen@12345")
        user.save()

    dependencies = [

    ]

    operations = [
        migrations.RunPython(seed_data),
    ]
