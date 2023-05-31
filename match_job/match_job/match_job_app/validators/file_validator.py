from django.core.exceptions import ValidationError

class FileInputValidator:
    def __init__(self, file) -> None:
        self.file = file

    def allowed_size(self, size_MB: int) -> bool | ValidationError:
        size_MB *= 1048576
        if self.file.size > size_MB:
            raise ValidationError(
                f"Przesłany obraz ma za duży rozmiar. Dozwolony rozmiar to {size_MB}MB."
            )
        else:
            return True
