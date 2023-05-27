
class ContextValidator:
    def __init__(self, context: dict, required_fields: list, error_message: str) -> None:
        self.context = context
        self.required_fields = required_fields
        self.error_message = error_message
        self.validate_context()
        
    def validate_context(self):
        for key in self.context:
            if key not in self.required_fields:
                print(key)
                raise KeyError("Кастомная ошибка валидации" + key + "not in required_fields" + self.error_message)
        self.validted_data = list(self.context.values())

