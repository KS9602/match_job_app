from string import ascii_letters
from django.core.exceptions import ValidationError


class StringInputValidator:
    ascii_letters_list = [letter for letter in ascii_letters]
    polish_letter = ascii_letters_list + ["ą", "ć", "ę", "ł", "ń", "ó", "ś", "ź", "ż"]
    allowed_special_characters = ["-", " ", "'"]

    def __init__(self, text: str) -> None:
        self.text = text

    def only_basic_asci_letter(self) -> bool | ValidationError:
        for letter in self.text:
            if letter not in (
                StringInputValidator.ascii_letters_list
                + StringInputValidator.allowed_special_characters
            ):
                raise ValidationError(f"Użyto niedozwolonego znaku {letter}")

        return True

    def only_polish_letter(self) -> bool | ValidationError:
        for letter in self.text:
            if letter not in (
                StringInputValidator.polish_letter
                + StringInputValidator.allowed_special_characters
            ):
                raise ValidationError(f"Użyto niedozwolonego znaku {letter}")

        return True

    def space_check(self) -> bool | ValidationError:
        """Only one spac in a row."""

        for index in range(len(self.text) - 1):
            if self.text[index] + self.text[index + 1] == "  ":
                raise ValidationError("Więcej niż jedna spacja jest niedozwolona")

        return True


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
