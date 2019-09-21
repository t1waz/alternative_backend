from django.core.exceptions import ValidationError


class SimpleValidator:
    def __init__(self, *args):
        self.fields = args

    def set_context(self, serializer):
        self.instance = getattr(serializer, 'instance', None)
        self.updated_fields = [field for field in dir(self) if field in self.fields]

    def run_validators(self, value):
        validators = getattr(self, 'validators')

        for validator in validators:
            try:
                validator(**value)
            except:  # TODO
                raise ValidationError('incorrect data for {}'.format(validator))  # TODO

    def __call__(self, value):
        common_fields = set(self.fields).intersection(set(self.updated_fields))
        if not self.instance or common_fields:
            self.run_validators(value)