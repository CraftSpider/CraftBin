"""
    Classes and methods to help with minecraft Model objects
"""

import json
import copy
import utils.vector as vector
import utils.rotator as rotator
import PIL.Image as Image

from . import state


class Model:

    __slots__ = ("namespace", "name", "_effective_data", "_raw_data", "parent", "textures", "ambient_occlusion",
                 "elements")

    UP_IDS = {"up": (0, 3), "down": (7, 4), "north": (1, 4), "south": (2, 7), "east": (3, 5), "west": (0, 6)}

    def __init__(self, namespace, name, data):
        self.namespace = namespace
        self.name = name
        self._raw_data = data
        self.parent = None
        if "parent" in data:
            self.parent = self.get_model(namespace, data["parent"])
        data = self._get_effective()

        self._effective_data = data
        self.ambient_occlusion = data.get("ambientocclusion", True)
        self.elements = data.get("elements", [])
        self.textures = data.get("textures", None)

    def __repr__(self):
        return f"Model(name: {self.name}, parent: {self.parent.name if self.parent else None})"

    def _get_effective(self):
        data = copy.deepcopy(self._raw_data)
        if self.parent is not None:
            par_data = copy.deepcopy(self.parent._effective_data)
            par_texs = par_data.get("textures", {})
            par_data.update(data)
            par_texs.update(data.get("textures", {}))
            par_data["textures"] = par_texs
            data = par_data
        return data

    def _resolve_texture(self, name):
        tex = self.textures.get(name, "")
        while tex.startswith("#"):
            tex = self.textures.get(tex[1:], "")
        return tex or None

    def _resolve_side_rotation(self, x, y, z):
        rot = rotator.Rotator(x, y, z)
        vecs = [
            vector.Vector(-1, 1, -1),
            vector.Vector(1, 1, -1),
            vector.Vector(-1, 1, 1),
            vector.Vector(1, 1, 1),
            vector.Vector(-1, -1, -1),
            vector.Vector(1, -1, -1),
            vector.Vector(-1, -1, 1),
            vector.Vector(1, -1, 1)
        ]

        for i in range(len(vecs)):
            vecs[i] = rot * vecs[i]

        up = []
        for i in range(len(vecs)):
            if vecs[i].y > 0:
                up.append(i)

        # Get model side and rotation
        m_side = None
        for side in self.UP_IDS:
            ids = self.UP_IDS[side]
            if ids[0] in up and ids[1] in up:
                m_side = side
                break
        m_rotation = None
        tl = vecs[self.UP_IDS[m_side][0]]
        if tl.z == -1 and tl.x == -1:
            m_rotation = 0
        elif tl.z == -1 and tl.x == 1:
            m_rotation = 90
        elif tl.z == 1 and tl.x == 1:
            m_rotation = 180
        elif tl.z == 1 and tl.x == -1:
            m_rotation = 270

        return m_side, m_rotation

    def inherits(self, name):
        if name == self.name:
            return True
        elif self.parent is None:
            return False
        else:
            return self.parent.inherits(name)

    def get_top(self, *, x=0, y=0, z=0):
        config = state.get_config()
        tex_base = config.resource_path / self.namespace / "textures"

        side, rotation = self._resolve_side_rotation(x, y, z)
        if side is None or rotation is None:
            raise ArithmeticError("Invalid block rotation")

        # TODO: Generate that side's texture from model
        # Temporary hack instead of model interpolation
        if self.inherits("block/cube"):
            tex = self._resolve_texture(side)
            if tex is None:
                return None
            img: Image.Image = Image.open(tex_base / (tex + ".png"))
            img = img.rotate(rotation)
            return img

        elif "all" in self.textures:
            tex_path = tex_base / f"{self.textures['all']}.png"
            return Image.open(tex_path)
        elif "texture" in self.textures:
            tex_path = tex_base / f"{self.textures['texture']}.png"
            return Image.open(tex_path)

    def get_sprite(self):
        # TODO: Get sprites for objects with no top view
        return None

    @classmethod
    def get_model(cls, namespace, name):
        block = f"{namespace}:{name}"
        config = state.get_config()
        models = config.models
        if block not in models:
            with open(config.resource_path / namespace / "models" / f"{name}.json") as file:
                data = json.load(file)
            models[block] = cls(namespace, name, data)
        return models[block]
