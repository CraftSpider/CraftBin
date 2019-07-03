
import abc

from .errors import ConversionError, UnknownConversion


class Converter(abc.ABC):

    @abc.abstractmethod
    def convert(self, data): ...


_TYPE_MAP = {}


def register_type(_type, converter):
    _TYPE_MAP[_type] = converter


def handle_conversion(data, annotation):
    if issubclass(annotation, Converter):
        converter = annotation()
    else:
        _converter_type = _TYPE_MAP.get(annotation, None)
        if _converter_type is None:
            raise UnknownConversion()
        converter = _converter_type()
    try:
        return converter.convert(data)
    except Exception:
        raise ConversionError


class StringConverter(Converter):

    def convert(self, data):
        return str(data)


class BytesConverter(Converter):

    def convert(self, data):
        return bytes(data)


class IntConverter(Converter):

    def convert(self, data):
        return int(data)


class FloatConverter(Converter):

    def convert(self, data):
        return float(data)


register_type(str, StringConverter)
register_type(bytes, BytesConverter)
register_type(int, IntConverter)
register_type(float, FloatConverter)
