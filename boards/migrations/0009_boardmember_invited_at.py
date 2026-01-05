# This migration was created but is no longer needed as invited_at was removed
# Keeping file for migration chain integrity

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0008_board_owner_boardmember'),
    ]

    operations = [
        # No operations - invited_at field removed from model
    ]
