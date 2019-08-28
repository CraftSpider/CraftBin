
import json
import random

from . import model, state


class Variant:

    __slots__ = ("model", "x", "y", "uv_lock", "weight")

    def __init__(self, namespace, data):
        self.model = model.Model.get_model(namespace, f"block/{data['model']}")
        self.x = data.get("x", 0)
        self.y = data.get("y", 0)
        self.uv_lock = data.get("uvlock", False)
        self.weight = data.get("weight", 100)

    def __repr__(self):
        return f"Variant(model={repr(self.model)}, x={self.x}, y={self.y}, uv_lock={self.uv_lock}, weight={self.weight})"

    def get_side(self, side):
        return self.model.get_side(side, x=self.x, y=self.y)

    def get_side_height(self, side):
        return self.model.get_side_height(side, x=self.x, y=self.y)

    def get_sprite(self):
        return self.model.get_sprite()


class Part:

    __slots__ = ("condition", "variant")

    def __init__(self, namespace, data):
        var = data["apply"]
        if isinstance(var, list):
            self.variant = [Variant(namespace, x) for x in var]
        else:
            self.variant = Variant(namespace, var)
        self.condition = data.get("when", None)

    def __repr__(self):
        return f"Part(condition={self.condition}, variant={repr(self.variant)})"

    def check_condition(self, x, y, z):
        if self.condition is None:
            return True
        # TODO: Finish condition checking
        config = state.get_config()

        for dir in ('north', 'south', 'east', 'west'):
            loc = [x, y, z]
            if dir == 'north':
                loc[2] -= 1
            elif dir == 'south':
                loc[2] += 1
            elif dir == 'west':
                loc[0] -= 1
            elif dir == 'east':
                loc[0] += 1
            if dir in self.condition:
                case = bool(self.condition[dir])
                try:
                    _, block, _ = config.schematic.get_block(*loc)
                    if block == "air":
                        return not case
                except AttributeError:
                    return not case

        return True

    def get_variant(self):
        variant = self.variant
        if isinstance(variant, list):
            variant = random.choices(variant, weights=[x.weight for x in variant])
        return variant


class Blockstate:

    __slots__ = ("namespace", "name", "multipart", "variants", "parts")

    def __init__(self, namespace, name, data):
        self.namespace = namespace
        self.name = name
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
                key = frozenset(tuple(x.split("=")) for x in variables)
                self.variants[key] = var

    def __repr__(self):
        return f"Blockstate(namespace={self.namespace}, name={self.name}, multipart={self.multipart})"

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
            elif kwargs[arg] is None:
                kwargs[arg] = ""
        key = frozenset((name, kwargs[name]) for name in kwargs)
        variant = self.variants.get(key, None)
        if isinstance(variant, list):
            variant = random.choices(variant, weights=[x.weight for x in variant])
        return variant

    # If using multiparts, use these:

    def get_parts(self):
        return self.parts

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
                blockstates[block] = cls(namespace, name, data)
        return blockstates[block]
