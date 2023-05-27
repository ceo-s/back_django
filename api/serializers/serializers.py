from api.services.validators import ContextValidator
from rest_framework import serializers


class BulkUpdateOrCreateListSerializer(serializers.ListSerializer):

    def update(self, instance, validated_data):
        validator = ContextValidator(self.context, ["model", "fields", "foreign_keys_fields"],
                                     error_message="Ошибка в diet_serializers.BulkUpdateOrCreateListSerializer !")
        model, fields, foreign_keys_fields = validator.validted_data

        instance_mapping = {item.id: item for item in instance}

        for_update = []
        for_create = []
        active_ids = set()
        for data in validated_data:
            id = data.get('id', 0)
            active_ids.add(id)
            instance = instance_mapping.get(id, None)
            if instance:
                for field in fields:
                    setattr(instance, field, data.get(field))
                for_update.append(instance)
            else:
                for field in foreign_keys_fields:
                    data[field + "_id"] = data.pop(field)["id"]

                data.pop("id", None)
                for_create += [model(**data)]

        model.objects.bulk_update(for_update, fields=fields)
        bulk_created = model.objects.bulk_create(for_create)

        for id, instance in instance_mapping.items():
            if id not in active_ids:
                instance.delete()

        return (for_update, bulk_created)
