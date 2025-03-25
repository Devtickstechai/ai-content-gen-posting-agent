from django.db import models, connection
from django.apps import apps

def create_dynamic_table(keyword):
    table_name = f'scraped_posts_{keyword.replace(" ", "_").lower()}'
    model_name = f"{keyword.capitalize()}Post"

    with connection.cursor() as cursor:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        print(f"🗑️ Dropping existing table: {table_name}")

    # Unregister model if already exists
    registered_models = apps.all_models['scraper_app']
    if model_name.lower() in registered_models:
        try:
            del registered_models[model_name.lower()]
            apps.clear_cache()
            print(f"🔥 Unregistered old model: {model_name}")
        except Exception as e:
            print(f"⚠️ Error unregistering {model_name}: {e}")

    # Define the model dynamically
    class Meta:
        db_table = table_name
        app_label = 'scraper_app'

    DynamicPost = type(model_name, (models.Model,), {
        'content': models.TextField(),
        'author': models.CharField(max_length=255),
        'likes': models.IntegerField(default=0),
        'comments': models.IntegerField(default=0),
        'shares': models.IntegerField(default=0),
        'timestamp': models.CharField(max_length=255),
        '__module__': __name__,
        'Meta': Meta
    })

    # Register the model properly in Django ORM
    apps.register_model('scraper_app', DynamicPost)

    # Create the table in the database
    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(DynamicPost)

    print(f"✅ Created table: {table_name}")
    return DynamicPost
