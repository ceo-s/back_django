from coaching.models import Client, ClientStatsActive, ClientBaseExercises
from api.serializers.coaching_serializers import ClientSerializer, ClientStatsActiveSerializer,\
    ClientBaseExercisesSerializer


def get_client_info(id):
    client = Client.objects.get(id=id)
    stats = ClientStatsActive.objects.get(client=client)
    base_exercises = ClientBaseExercises.objects.get(client=client)

    # return [ClientSerializer(client), ClientStatsActiveSerializer(stats), ClientBaseExercisesSerializer(base_exercises)]
    return {"client": ClientSerializer(client).data,
            "stats": ClientStatsActiveSerializer(stats).data,
            "base_exercises": ClientBaseExercisesSerializer(base_exercises).data}


def perform_update(data, serializer, context, many=False, **filter_params):
    """
    Вызывает update метод по входным параметрам.
    """
    model = context.get("model")
    instance = model.objects.filter(
        **filter_params) if many else model.objects.get(**filter_params)
    print("DATA", data)
    serializer = serializer(instance=instance, data=data,
                            context=context,
                            many=many)
    if serializer.is_valid():
        return serializer.save()

    else:
        raise Exception(
            f"My Custom Error. Serializer data is not valid.\n Error message: {serializer.errors}")
