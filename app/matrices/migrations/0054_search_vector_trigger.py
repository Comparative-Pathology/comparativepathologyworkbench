from django.contrib.postgres.search import SearchVector
from django.db import migrations


def compute_search_vector(apps, schema_editor):
    Image = apps.get_model('matrices', 'Image')
    Image.objects.update(search_vector=SearchVector('name', 'comment'))


class Migration(migrations.Migration):

    dependencies = [
        ('matrices', '0053_image_search_vector_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            CREATE TRIGGER search_vector_trigger
            BEFORE INSERT OR UPDATE OF name, comment, search_vector
            ON matrices_image
            FOR EACH ROW EXECUTE PROCEDURE
            tsvector_update_trigger(
                search_vector, 'pg_catalog.english', name, comment
            );
            UPDATE matrices_image SET search_vector = NULL;
            """,
            reverse_sql="""
            DROP TRIGGER IF EXISTS search_vector_trigger
            ON matrices_image;
            """,
        ),
        migrations.RunPython(
            compute_search_vector, reverse_code=migrations.RunPython.noop
        ),
    ]
