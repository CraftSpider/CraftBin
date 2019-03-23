
import json

from . import model, state


class Variant:

    __slots__ = ("model", "x", "y", "uv_lock", "weight")

    def __init__(self, namespace, data):
        self.model = model.Model.get_model(namespace, f"block/{data['model']}")
        self.x = data.get("x", 0)
        self.y = data.get("y", 0)
        self.uv_lock = data.get("uvlock", False)
        self.weight = data.get("weight", 100)


class Part:

    __slots__ = ("condition", "variant")

    def __init__(self, namespace, data):
        var = data["apply"]
        if isinstance(var, list):
            self.variant = [Variant(namespace, x) for x in var]
        else:
            self.variant = Variant(namespace, var)
        self.condition = data.get("when", None)


class Blockstate:

    __slots__ = ("multipart", "variants", "parts")

    def __init__(self, namespace, data):
        variants = data.get("variants", None)
        if not variants:
            self.variants = None
            self.multipart = True
            self.parts = [Part(namespace, item) for item in data["multipart"]]
        else:
            self.variants = {}
            self.multipart = False
            self.parts = None

            # Fill variants
            for name in variants:
                data = variants[name]
                if isinstance(data, list):
                    var = [Variant(namespace, var) for var in data]
                    if var[0].weight == 100:
                        for v in var:
                            v.weight = 100 / len(var)
                else:
                    var = Variant(namespace, data)

                variables = name.split(",")
                key = frozenset(tuple(x.split("=")) if len(x.split("=")) > 1 else tuple([x, None]) for x in variables)
                self.variants[key] = var

    def is_variant(self):
        return not self.multipart

    def is_multipart(self):
        return self.multipart

    # If using variants, use these:

    def has_variable(self, name):
        for key in self.variants:
            for item in key:
                if item[0] == name:
                    return True
        return False

    def get_variant(self, **kwargs):
        for arg in kwargs:
            if kwargs[arg] is True:
                kwargs[arg] = "true"
            elif kwargs[arg] is False:
                kwargs[arg] = "false"
        key = frozenset((name, kwargs[name]) for name in kwargs)
        return self.variants.get(key, None)

    # If using multiparts, use these:

    # Factory function:

    @classmethod
    def get_blockstate(cls, namespace, name):
        block = f"{namespace}:{name}"
        config = state.get_config()
        blockstates = config.blockstates
        if block not in blockstates:
            path = config.resource_path / namespace / "blockstates" / f"{name}.json"
            with open(path) as file:
                data = json.load(file)
                blockstates[block] = cls(namespace, data)
        return blockstates[block]
