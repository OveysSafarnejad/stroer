# -*- coding: utf-8 -*-
"""
core structs module.
"""

import inspect
from abc import abstractmethod
from collections import OrderedDict
from copy import deepcopy
from threading import Lock


class SingletonMetaBase(type):
    """
    singleton meta base class.

    this is a thread-safe implementation of singleton.
    """

    _lock = Lock()

    def __call__(cls, *args, **kwargs):
        if cls._has_instance() is False:
            with cls._lock:
                if cls._has_instance() is False:
                    instance = super().__call__(*args, **kwargs)
                    cls._register_instance(instance)

        return cls._get_instance()

    @abstractmethod
    def _has_instance(cls):
        """
        gets a value indicating there is a registered instance.

        :raises NotImplementedError: not implemented error.

        :rtype: bool
        """

        raise NotImplementedError()

    @abstractmethod
    def _register_instance(cls, instance):
        """
        registers the given instance.

        :param object instance: instance to be registered.

        :raises NotImplementedError: not implemented error.
        """

        raise NotImplementedError()

    @abstractmethod
    def _get_instance(cls):
        """
        gets the registered instance.

        :raises NotImplementedError: not implemented error.

        :rtype: object
        """

        raise NotImplementedError()


class EnumMember:
    """
    enum member class.

    if you need localizable values for your enumerations, you could define
    enum values of this type instead of primitive types.

    for example:

    class Animal(EnumBase):
        RABBIT = EnumMember(1, 'Rabbit')
        LION = EnumMember(2, 'Lion')
        UNKNOWN = 3

    animal_1 = Animal.RABBIT --> this returns the value of rabbit which is 1.
    animal_1_name = Animal(Animal.RABBIT) --> this returns the name of rabbit
    which is `Rabbit`.
    animal_2 = Animal.UNKNOWN --> this returns the value of unknown which is 3.
    animal_2_name = Animal(3) --> this returns the name of unknown which is `UNKNOWN`.
    animal_5 = Animal(5, silent=True) --> this returns None.
    animal_6 = Animal(6) --> this raises an attribute error.

    as you could see, you could also define enum values with primitive types if needed.
    but they won't have localizable names.
    """

    def __init__(self, value, name):
        """
        initializes an instance of EnumMember.

        :param value: enum value.
        :param str name: enum name.
        """

        self._value = value
        self._name = name

    def __str__(self):
        """
        gets the string representation of this enum member.

        :rtype: str
        """

        return self.name

    def __repr__(self):
        """
        gets the string representation of this enum member.

        :rtype: str
        """

        return '[{value}:{name}]'.format(value=self.value, name=self.name)

    def __eq__(self, other):
        """
        gets a value indicating that this enum value is equal to provided value.

        :param EnumMember | object other: other object to be compared
                                          to this enum member.

        :rtype: bool
        """

        if isinstance(other, EnumMember):
            return self.value == other.value

        return self.value == other

    def __ne__(self, other):
        """
        gets a value indicating that this enum value is not equal to provided value.

        :param EnumMember | object other: other object to be compared
                                          to this enum member.

        :rtype: bool
        """

        if isinstance(other, EnumMember):
            return self.value != other.value

        return self.value != other

    def __ge__(self, other):
        """
        implements `>=` operator to compare current enum member with provided value.

        :param EnumMember | object other: other object to be compared
                                          to this enum member.

        :rtype: bool
        """

        if isinstance(other, EnumMember):
            return self.value >= other.value

        return self.value >= other

    def __le__(self, other):
        """
        implements `<=` operator to compare current enum member with provided value.

        :param EnumMember | object other: other object to be compared
                                          to this enum member.

        :rtype: bool
        """

        if isinstance(other, EnumMember):
            return self.value <= other.value

        return self.value <= other

    def __gt__(self, other):
        """
        implements `>` operator to compare current enum member with provided value.

        :param EnumMember | object other: other object to be compared
                                          to this enum member.

        :rtype: bool
        """

        if isinstance(other, EnumMember):
            return self.value > other.value

        return self.value > other

    def __lt__(self, other):
        """
        implements `<` operator to compare current enum member with provided value.

        :param EnumMember | object other: other object to be compared
                                          to this enum member.

        :rtype: bool
        """

        if isinstance(other, EnumMember):
            return self.value < other.value

        return self.value < other

    def __hash__(self):
        """
        gets the hash of this enum member.

        :rtype: int
        """

        return hash(self.value)

    @property
    def value(self):
        """
        gets this enum member's value.

        :returns: object
        """

        return self._value

    @property
    def name(self):
        """
        gets this enum member's name.

        :rtype: str
        """

        return self._name


class CoreEnumMeta(type):
    """
    core enum metaclass.
    """

    # each enum class will gain it's own attributes to save names and values of
    # it's members. the below attributes will always remain None and never get populated.
    __enum_names = None
    __enum_values = None
    __enum_dict = None
    __enum_tuples = None

    @staticmethod
    def __new__(mcs, *args, **kwargs):
        """
        creates and returns a new class.

        note that this method will only get called once per each enum subclass.

        :rtype: type[CoreEnumMeta]
        """

        mcs._check_duplicates(args[0], args[2])
        return super().__new__(mcs, *args, **kwargs)

    def __getattribute__(cls, name):
        """
        gets an attribute of this class with given name.

        it returns the enum value, even if it is of `EnumMember` type.

        :param str name: attribute name to be get.

        :returns: object
        """

        member = type.__getattribute__(cls, name)
        # we should not call 'get_pure_value' here because it results in recursion error.
        if isinstance(member, EnumMember):
            member = member.value

        return member

    def __contains__(cls, member):
        """
        gets a value indicating that given input exists in the enumeration values.

        this method is overridden to be able to check
        for existence with `in` keyword. for example:
        has_value = 'value' in SomeEnum

        :param EnumMember | object member: value to be checked for existence.

        :rtype: bool
        """

        member = cls.get_pure_value(member)
        return member in cls.values()

    def __to_dict(cls):
        """
        gets a dict containing all values of this enum and their names.

        :returns: dict(object value, str name)
        :rtype: dict
        """

        if cls.__enum_dict is None:
            cls._populate_members()

        return cls.__enum_dict

    @staticmethod
    def _check_duplicates(enum, attrs):
        """
        checks that is there any enum members with the same value.

        if it does, it raises an error.

        :param str enum: enum name.
        :param dict attrs: all attributes of this class.

        :raise ValueError: value error.
        """

        values = []
        for name, value in attrs.items():
            if CoreEnumMeta._is_enumeration(name, value):
                pure_value = CoreEnumMeta.get_pure_value(value)
                if pure_value in values:
                    raise ValueError('Enumeration [{enum}] has multiple '
                                     'members with value [{value}].'
                                     .format(enum=enum, value=pure_value))

                values.append(pure_value)

    @staticmethod
    def _is_enumeration(name, value):
        """
        gets a value indicating that given name belongs to an enum member.

        enum members must not start or end with underscores `_`.
        callable values are also ignored.
        all `EnumMember` instances will be accepted without considering their naming style.

        :param str name: name to be checked.
        :param EnumMember | object value: value to be checked.

        :rtype: bool
        """

        if isinstance(value, EnumMember):
            return True

        if name is None or value is None or callable(value) or \
                inspect.isfunction(value) or inspect.ismethod(value) or \
                inspect.ismethoddescriptor(value) or inspect.isclass(value):
            return False

        return not name.startswith('_') and not name.endswith('_')

    @staticmethod
    def get_pure_value(member):
        """
        gets the pure value of given value.

        if the value is an instance of `EnumMember` it returns the `value` of it.
        otherwise it returns the same input.

        :param EnumMember | object member: value to get its pure value.

        :returns: object
        """

        if isinstance(member, EnumMember):
            return member.value

        return member

    def _populate_members(cls):
        """
        populates this enum's names and values and dictionary.
        """

        names = []
        values = []
        dictionary = OrderedDict()
        for name in cls.__dict__:
            item = cls.__dict__.get(name)
            if cls._is_enumeration(name, item):
                if isinstance(item, EnumMember):
                    name = item.name
                    item = item.value
                names.append(name)
                values.append(item)
                dictionary[item] = name

        cls.__enum_names = tuple(names)
        cls.__enum_values = tuple(values)
        cls.__enum_dict = dictionary
        cls.__enum_tuples = tuple(dictionary.items())

    def values(cls):
        """
        gets a tuple containing all values in the enumeration.

        :rtype: tuple
        """

        if cls.__enum_values is None:
            cls._populate_members()

        return cls.__enum_values

    def names(cls):
        """
        gets a tuple containing all names in the enumeration.

        :rtype: tuple
        """

        if cls.__enum_names is None:
            cls._populate_members()

        return cls.__enum_names

    def to_dict(cls):
        """
        gets a dict containing all values of this enum and their names.

        :returns: dict(object value, str name)
        :rtype: dict
        """

        return deepcopy(cls.__to_dict())

    def to_tuple(cls):
        """
        gets a tuple of tuples containing all values of this enum and their names.

        the result of this method could be used as `choices` in django model field.

        :returns: tuple[tuple[object value, str name]]
        :rtype: tuple[tuple]
        """

        if cls.__enum_tuples is None:
            cls._populate_members()

        return cls.__enum_tuples

    def _get_value(cls, name):
        enum_dict = cls.__to_dict()
        key_list = list(enum_dict.keys())
        value_list = list(enum_dict.values())
        position = value_list.index(name)

        return key_list[position]

    def str(cls, value, reverse=False):
        """
        gets the name of given value in enumeration.

        note that if the value is not an `EnumMember` instance, it does not have
        a name and the name of it's attribute will be returned instead.
        if the value does not exist in enumeration, it raises an error.

        :param EnumMember | object value: value to get its name.
        :param Boolean | reverse: boolean to get its value instead of name.

        :raises AttributeError: attribute error.

        :rtype: str
        """

        value = cls.get_pure_value(value)
        name = cls.__to_dict().get(value)

        if reverse is True:
            return cls._get_value(value)

        if name is None:
            raise AttributeError('Enumeration [{enum}] does not have '
                                 'a member with value [{value}].'
                                 .format(enum=cls.__name__, value=value))

        return str(name)


class EnumBase(metaclass=CoreEnumMeta):
    """
    enum base class.

    all application enumerations must inherit from this class.
    """

    @staticmethod
    def __new__(cls, value, silent=False, reverse=False):
        """
        gets the name of given value in enumeration.

        note that if the value is not an `EnumMember` instance, it does not have
        a name and the name of it's attribute will be returned instead.
        if the value does not exist in enumeration, it raises an error.

        example usage:

        class CarEnum(EnumBase):
            MERCEDES = EnumMember(1, 'Mercedes')
            BMW = 2

        name1 = CarEnum(1) --> `Mercedes`
        name2 = CarEnum(CarEnum.MERCEDES) --> `Mercedes`
        name3 = CarEnum(2000, silent=True) --> None
        name4 = CarEnum(2000) --> raises AttributeError
        name5 = CarEnum(2) --> `BMW`

        :param EnumMember | object value: value to get its name.

        :param bool silent: specifies that if value does not exist in
                            enumeration, does not raise an error and
                            return None instead. defaults to False.

        :raises AttributeError: attribute error.

        :rtype: str
        """

        if silent is True:
            return cls.try_str(value, reverse)

        return cls.str(value, reverse)

    @classmethod
    def contains(cls, value):
        """
        gets a value indicating that given input exists in the enumeration values.

        :param EnumMember | object value: value to be checked for existence.

        :rtype: bool
        """

        value = cls.get_pure_value(value)
        return value in cls.values()

    @classmethod
    def try_str(cls, value, reverse=False):
        """
        gets the name of given value in enumeration.

        note that if the value is not an `EnumMember` instance, it does not have
        a name and the name of it's attribute will be returned instead.
        if the value does not exist in enumeration, it returns None.

        :param EnumMember | object value: value to get its name.
        :param Boolean | object reverse: boolean to do reverse.

        :rtype: str
        """

        try:
            return cls.str(value, reverse)
        except (AttributeError, ValueError):
            return None
