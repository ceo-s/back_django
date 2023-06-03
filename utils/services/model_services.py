class PathGenerator:
    """
    Generates custom path for django ImageField and FileField.\n
    Requires field name to make it part of path.\n
    Output format:\n
        "model_name/field_value/filename.ext
    """

    def __init__(self, field: str):
        self.field = field

    def __call__(self, instanse, filename):
        name, ext = filename.split(".")
        filename = name[:20] + "." + ext
        path = self.generate_path(instance=instanse, filename=filename)
        return path

    def generate_path(self, instance, filename):
        """
        Making custom path for uploading files.
        """
        model_name = getattr(instance, "_meta").model_name
        field_value = getattr(instance, self.field)

        print(instance.__dict__)
        return f"{model_name}/{field_value}/{filename}"
