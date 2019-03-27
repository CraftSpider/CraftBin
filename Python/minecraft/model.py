"""
    Classes and methods to help with minecraft Model objects
"""

import json
import copy
import utils.vector as vector
import utils.rotator as rotator
import PIL.Image as Image
import PIL.ImageColor as Color
import PIL.ImageEnhance as Enhance

from . import state, enums


class Rotation:

    __slots__ = ("origin", "axis", "angle", "rescale")

    def __init__(self, data):
        self.origin = vector.Vector(*data["origin"])
        self.axis = getattr(vector, f"Unit{data['axis'].upper()}")
        self.angle = data["angle"]
        self.rescale = data.get("rescale", False)

    def __repr__(self):
        return f"Rotation(origin={repr(self.origin)}, axis={repr(self.axis)}, angle={self.angle}, " + \
               f"rescale={self.rescale})"


class Face:

    __slots__ = ("side", "uv", "texture", "cull_face", "rotation", "tint_index")

    def __init__(self, side, data):
        self.side = enums.Side[side.upper()]
        self.uv = data.get("uv", None)
        if self.uv is not None:
            self.uv = tuple(self.uv)
        self.texture = data["texture"]
        cull_face = data.get("cullface", None)
        if cull_face is not None:
            self.cull_face = enums.Side[cull_face.upper()]
        else:
            self.cull_face = self.side
        self.rotation = data.get("rotation", 0)
        self.tint_index = data.get("tintindex", None)

    def __repr__(self):
        return f"Face(side={self.side}, uv={self.uv}, texture={self.texture}, cull_face={self.cull_face}, " + \
               f"rotation={self.rotation}, tint_index={self.tint_index})"


class Element:

    __slots__ = ("begin", "end", "rotation", "shade", "faces")

    def __init__(self, data):
        self.begin = vector.Vector(*data["from"])
        self.end = vector.Vector(*data["to"])
        self.rotation = Rotation(data["rotation"]) if "rotation" in data else None
        self.shade = data.get("shade", True)
        self.faces = [Face(x, data["faces"][x]) for x in data["faces"]]

    def __repr__(self):
        return f"Element(begin={repr(self.begin)}, end={repr(self.end)}, rotation={repr(self.rotation)}, " + \
               f"shade={self.shade}, faces={repr(self.faces)})"

    def get_face(self, side):
        for face in self.faces:
            if face.side == side:
                return face
        return None


class Model:

    __slots__ = ("namespace", "name", "_effective_data", "_raw_data", "parent", "textures", "ambient_occlusion",
                 "elements")

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
        self.elements = [Element(x) for x in data.get("elements", ())]
        self.textures = data.get("textures", None)

    def __repr__(self):
        parent = self.parent.name if self.parent else None
        return f"Model(namespace={self.namespace}, name={self.name}, parent={parent})"

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

    def inherits(self, name):
        if name == self.name:
            return True
        elif self.parent is None:
            return False
        else:
            return self.parent.inherits(name)

    def get_texture(self, name):
        if name.startswith("#"):
            name = name[1:]
        tex = self.textures.get(name, "")
        while tex.startswith("#"):
            tex = self.textures.get(tex[1:], "")
        return tex or None

    def get_top(self, *, x=0, y=0, z=0):
        config = state.get_config()
        tex_base = config.resource_path / self.namespace / "textures"

        side, rotation = _resolve_side_rotation(x, y, z)
        if side is None or rotation is None:
            raise ArithmeticError("Invalid block rotation")

        blank = Image.new("RGBA", (config.block_size, config.block_size), Color.getrgb("white"))
        out = Image.new("RGBA", (config.block_size, config.block_size), Color.getrgb("white"))
        for element in self.elements:
            face = element.get_face(side)
            if face is None:
                continue
            axis = side.axis
            factor = _resolve_darken(element, axis)
            tex = self.get_texture(face.texture)
            if tex is None:
                print(f"Resolved texture for model {self.namespace}:{self.name} is invalid: {face.texture}")
                return None
            img = Image.open(tex_base / (tex + ".png"))
            img.crop(_resolve_uv(element, face, side))
            img = Enhance.Brightness(img).enhance(factor)
            # Add the correct portion of the texture based on cube and depth
            mask = None
            if img.mode == "RGBA":
                mask = img.split()[3]
            out.paste(img, mask=mask)
        if out == blank:
            return None

        out = out.rotate(rotation)
        return out

    def get_sprite(self):
        config = state.get_config()
        tex_base = config.resource_path / self.namespace / "textures"
        item_name = "item" + self.name[5:]
        try:
            item_model = self.get_model(self.namespace, item_name)
        except FileNotFoundError:
            return None
        return Image.open(tex_base / (item_model.get_texture("layer0") + ".png"))

    @classmethod
    def get_model(cls, namespace, name):
        if name == "builtin/generated":
            return None
        block = f"{namespace}:{name}"
        config = state.get_config()
        models = config.models
        if block not in models:
            with open(config.resource_path / namespace / "models" / f"{name}.json") as file:
                data = json.load(file)
            models[block] = cls(namespace, name, data)
        return models[block]


def _resolve_side_rotation(x, y, z):
    rot = rotator.Rotator(x, y, z)
    vecs = vector.rect_list(vector.Vector(-1, 1, -1), vector.Vector(1, -1, 1))

    for i in range(len(vecs)):
        vecs[i] = rot * vecs[i]

    up = []
    for i in range(len(vecs)):
        if vecs[i].y > 0:
            up.append(i)

    # Get model side and rotation
    m_side = None
    for side in enums.Side:
        if side.tl in up and side.br in up:
            m_side = side
            break
    m_rotation = None
    tl = vecs[m_side.tl]
    if tl.z == -1 and tl.x == -1:
        m_rotation = 0
    elif tl.z == -1 and tl.x == 1:
        m_rotation = 90
    elif tl.z == 1 and tl.x == 1:
        m_rotation = 180
    elif tl.z == 1 and tl.x == -1:
        m_rotation = 270

    return m_side, m_rotation


def _resolve_uv(element, face, side):
    if face.uv is None:
        begin = element.begin
        end = element.end
        vecs = vector.rect_list(begin, end)
        tl = vecs[side.tl]
        br = vecs[side.br]

        if tl.x == br.x:
            return tl.y, tl.z, br.y, br.z
        elif tl.y == br.y:
            return tl.x, tl.z, br.x, br.z
        elif tl.z == br.z:
            return tl.x, tl.y, br.x, br.y
    else:
        return face.uv


def _resolve_darken(element, axis):
    neg = False
    if len(axis) == 2:
        neg = True
        axis = axis[1]
    pos_begin = getattr(element.begin, axis)
    pos_end = getattr(element.end, axis)
    if neg:
        pos = 16 - min(pos_begin, pos_end)
    else:
        pos = max(pos_begin, pos_end)
    factor = pos / 16
    return factor
