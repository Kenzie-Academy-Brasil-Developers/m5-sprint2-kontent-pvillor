class DataValidationError(Exception):
    ...


class ContentSerializer:
    valid_inputs = {
        "title": str,
        "module": str,
        "students": int,
        "description": str,
        "is_active": bool,
    }

    def __init__(self, *args, **kwargs):
        self.data = kwargs
        self.errors = {}

    def is_valid(self) -> bool:

        self.clean_data()

        try:
            self.validate_required_keys()
            self.validate_data_types()

            return True
        except DataValidationError:
            return False

    def clean_data(self):
        data_keys = tuple(self.data.keys())
        for key in data_keys:
            if key not in self.valid_inputs.keys():
                self.data.pop(key)

    def validate_required_keys(self):
        for valid_key in self.valid_inputs.keys():
            if valid_key not in self.data.keys():
                self.errors[valid_key] = "missing key"

        if self.errors:
            raise DataValidationError

    def validate_data_types(self):
        for valid_key, valid_type in self.valid_inputs.items():
            if type(self.data[valid_key]) is not valid_type:

                self.errors.update(
                    {valid_key: f"must be a {valid_type.__name__}"}
                )

        if self.errors:
            raise DataValidationError