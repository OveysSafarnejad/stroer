import random
import string


def random_generate(size=26, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def generate_slug(model, search_field, length=6):
    """
    generate slug for model.

    :param type model: the model class.
    :param int length: length of generated slug.

    :rtype: str
    """

    generated_slug = random_generate(length)
    filters = {}
    filters[search_field] = generated_slug
    existed = model.objects.filter(**filters).exists()
    if existed is True:
        return generate_slug(model, search_field, length)

    return generated_slug


def make_iterable(values, collection=None):
    """
    converts the provided values to iterable.

    it returns a collection of values using the given collection type.

    :param object | list[object] | tuple[object] | set[object] values: value or values to make
                                                                       iterable. if the values
                                                                       are iterable, it just
                                                                       converts the collection
                                                                       to given type.

    :param type[list | tuple | set] collection: collection type to use.
                                                defaults to list if not provided.

    :rtype: list | tuple | set
    """

    if collection is None:
        collection = list

    if values is None:
        return collection()

    if not isinstance(values, (list, tuple, set)):
        values = (values,)

    return collection(values)
