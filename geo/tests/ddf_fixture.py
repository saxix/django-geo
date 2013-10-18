from django_dynamic_fixture.fixture_algorithms.sequential_fixture import SequentialDataFixture


class DataFixture(SequentialDataFixture):

    def uuidfield_config(self, field, key):

        if hasattr(field, '_create_uuid'):
            value = field._create_uuid()
        elif hasattr(field, 'create_uuid'):
            value = field.create_uuid()
        else:
            value = None
        return str(value)
