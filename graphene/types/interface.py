from .field import Field
from .utils import yank_fields_from_attrs
from collections import OrderedDict

from .base import BaseOptions, BaseType


class InterfaceOptions(BaseOptions):
    fields = None  # type: Dict[str, Field]


class Interface(BaseType):
    '''
    Interface Type Definition

    When a field can return one of a heterogeneous set of types, a Interface type
    is used to describe what types are possible, what fields are in common across
    all types, as well as a function to determine which type is actually used
    when the field is resolved.
    '''
    @classmethod
    def __init_subclass_with_meta__(cls, **options):
        _meta = InterfaceOptions(cls)

        fields = OrderedDict()
        for base in reversed(cls.__mro__):
            fields.update(
                yank_fields_from_attrs(base.__dict__, _as=Field)
            )

        _meta.fields = fields
        super(Interface, cls).__init_subclass_with_meta__(_meta=_meta, **options)

    @classmethod
    def resolve_type(cls, instance, context, info):
        from .objecttype import ObjectType
        if isinstance(instance, ObjectType):
            return type(instance)

    def __init__(self, *args, **kwargs):
        raise Exception("An Interface cannot be intitialized")

    @classmethod
    def implements(cls, objecttype):
        pass
