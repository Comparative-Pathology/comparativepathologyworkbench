from django.contrib.postgres.search import SearchVector
from django.db import migrations


def compute_search_vector(apps, schema_editor):
    Image = apps.get_model('matrices', 'Collection')
    Image.objects.update(search_vector=SearchVector('title', 'description'))


class Migration(migrations.Migration):

    dependencies = [
        ('matrices', '0055_collection_search_vector_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            CREATE TRIGGER search_vector_trigger_collection
            BEFORE INSERT OR UPDATE OF title, description, search_vector
            ON matrices_collection
            FOR EACH ROW EXECUTE PROCEDURE
            tsvector_update_trigger(
                search_vector, 'pg_catalog.english', title, description
            );
            UPDATE matrices_collection SET search_vector = NULL;
            """,
            reverse_sql="""
            DROP TRIGGER IF EXISTS search_vector_trigger_collection
            ON matrices_collection;
            """,
        ),
        migrations.RunPython(
            compute_search_vector, reverse_code=migrations.RunPython.noop
        ),
    ]
