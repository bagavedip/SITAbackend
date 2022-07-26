from customers.models import Customer


class CustomerService:
    @staticmethod
    def get_queryset():
        return Customer.object.all()

    @staticmethod
    def get_tenant(schema_name):
        return CustomerService.get_queryset().get(schema_name=schema_name)
