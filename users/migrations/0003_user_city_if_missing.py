from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_payment"),
    ]

    operations = [
        migrations.RunSQL(
            sql="ALTER TABLE users_user ADD COLUMN IF NOT EXISTS city VARCHAR(150) NOT NULL DEFAULT '';",
            reverse_sql=migrations.RunSQL.noop,
            state_operations=[
                migrations.AddField(
                    model_name="user",
                    name="city",
                    field=models.CharField(
                        help_text="Укажите город",
                        max_length=150,
                        verbose_name="Город",
                    ),
                ),
            ],
        ),
    ]
