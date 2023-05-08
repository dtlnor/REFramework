import json
import fire
import os

code_typedefs = {
    "F32": "RSZFloat",
    "F64": "RSZDouble",
    "U8": "ubyte",
    "S8": "byte",
    "S64": "RSZInt64",
    "S32": "RSZInt",
    "S16": "RSZShort",
    "U64": "RSZUInt64",
    "U32": "RSZUInt",
    "U16": "RSZUShort"
}

def als(align, size):
    return { "align": align, "size": size }

hardcoded_align_sizes = {
    "Bool": als(1, 1),
    "C8": als(1, 1),
    "S8": als(1, 1),
    "U8": als(1, 1),

    "C16": als(2, 2),
    "S16": als(2, 2),
    "U16": als(2, 2),
    "F16": als(2, 2),
    
    "S32": als(4, 4),
    "U32": als(4, 4),
    "F32": als(4, 4),

    "S64": als(8, 8),
    "U64": als(8, 8),
    "F64": als(8, 8),

    "Object": als(4, 4),
    "UserData": als(4, 4),
    "Resource": als(4, 4),
    "String": als(4, 4),
    "RuntimeType": als(4, 4),

    "Quaternion": als(16, 16),
    "Guid": als(8, 16),
    "GameObjectRef": als(8, 16),
    "Color": als(4, 4),
    "DateTime": als(8, 8),

    "Uint2": als(4, 8),
    "Uint3": als(4, 12),
    "Uint4": als(4, 16),
    "Int2": als(4, 8),
    "Int3": als(4, 12),
    "Int4": als(4, 16),
    "Float2": als(4, 8),
    "Float3": als(4, 12),
    "Float4": als(4, 16),
    "Mat4": als(16, 64),
    "Vec2": als(16, 16),
    "Vec3": als(16, 16),
    "Vec4": als(16, 16),

    "AABB": als(16, 32),
    "Capsule": als(16, 48),
    "Cone": als(16, 32),
    "LineSegment": als(16, 32),
    "OBB": als(16, 80),
    "Plane": als(16, 16),
    "Point": als(4, 8),
    "Range": als(4, 8),
    "RangeI": als(4, 8),
    "Size": als(4, 8),
    "Sphere": als(16, 16),
    "Triangle": als(16, 48),
    "Cylinder": als(16, 48),
    "Area": als(16, 48),
    "Rect": als(4, 16),
    "Frustum": als(16, 96),
    "KeyFrame": als(16, 16),

    "Sfix": als(4, 4),
    "Sfix2": als(4, 8),
    "Sfix3": als(4, 12),
    "Sfix4": als(4, 16),
    

}

hardcoded_native_type_to_TypeCode = {
    # 'bool': 'Bool',
    # 'c8': 'C8',
    # 's8': 'S8',
    # 'u8': 'U8',

    # 'c16': 'C16',
    # 's16': 'S16',
    # 'u16': 'U16',
    # 'f16': 'F16',

    # 's32': 'S32',
    # 'u32': 'U32',
    # 'f32': 'F32',
    'float': 'F32',
    'int': 'S32',
    'size_t': 'U32',

    # 's64': 'S64',
    # 'u64': 'U64',
    # 'f64': 'F64',

    # 'Object': 'Object',
    # 'userdata': 'UserData',

    # typecode
    # 'Bool': 'Bool',
    # 'C8': 'C8',
    # 'C16': 'C16',
    # 'S8': 'S8',
    # 'U8': 'U8',
    # 'S16': 'S16',
    # 'U16': 'U16',
    # 'S32': 'S32',
    # 'U32': 'U32',
    # 'S64': 'S64',
    # 'U64': 'U64',
    # 'F32': 'F32',
    # 'F64': 'F64',
    # 'System.Object': 'Object',
    # 'via.GameObject': 'Object',
    # 'via.UserData': 'UserData',
    # 'Resource': 'Resource',
    # 'System.String': 'String',
    # 'System.RuntimeType': 'RuntimeType',
    # 'Object': 'Object',
    # 'UserData': 'UserData',
    # 'Resource': 'Resource',
    # 'String': 'String',
    # 'RuntimeType': 'RuntimeType',

    'System.Boolean': 'Bool',
    'System.Char': 'C8',
    # 'C16': 'C16',
    'System.SByte': 'S8',
    'System.Byte': 'U8',
    'System.Int16': 'S16',
    'System.UInt16': 'U16',
    'System.Int32': 'S32',
    'System.UInt32': 'U32',
    'System.Int64': 'S64',
    'System.UInt64': 'U64',
    # 'via.f16': 'F16',
    'System.Single': 'F32',
    'System.Double': 'F64',
    # 'System.Guid': 'Guid',
    # 'via.Guid': 'Guid',
    # 'via.vec2': 'Vec2',
    # 'via.vec3': 'Vec3',
    # 'via.vec4': 'Vec4',
}

hardcoded_type_code_mapping = {
    # typecode
    'System.Action': 'Action',
    'Struct': 'Struct',
    'NativeObject': 'NativeObject',
    'MBString': 'MBString',
    'System.Enum': 'Enum',
    'via.Uint2': 'Uint2',
    'via.Uint3': 'Uint3',
    'via.Uint4': 'Uint4',
    'via.Int2': 'Int2',
    'via.Int3': 'Int3',
    'via.Int4': 'Int4',
    'via.Float2': 'Float2',
    'via.Float3': 'Float3',
    'via.Float4': 'Float4',
    'via.Float3x3': 'Float3x3',
    'via.Float3x4': 'Float3x4',
    'via.Float4x3': 'Float4x3',
    'via.Float4x4': 'Float4x4',
    'via.Half2': 'Half2',
    'via.Half4': 'Half4',
    'via.mat3': 'Mat3',
    'via.mat4': 'Mat4',
    'via.vecU4': 'VecU4',
    'via.Quaternion': 'Quaternion',
    'via.Color': 'Color',
    'System.DateTime': 'DateTime',
    'via.AABB': 'AABB',
    'via.Capsule': 'Capsule',
    'via.TaperedCapsule': 'TaperedCapsule',
    'via.Cone': 'Cone',
    'via.Line': 'Line',
    'via.LineSegment': 'LineSegment',
    'via.OBB': 'OBB',
    'via.Plane': 'Plane',
    'via.PlaneXZ': 'PlaneXZ',
    'via.Point': 'Point',
    'via.Range': 'Range',
    'via.RangeI': 'RangeI',
    'via.Ray': 'Ray',
    'via.RayY': 'RayY',
    'via.Segment': 'Segment',
    'via.Size': 'Size',
    'via.Sphere': 'Sphere',
    'via.Triangle': 'Triangle',
    'via.Cylinder': 'Cylinder',
    'via.Ellipsoid': 'Ellipsoid',
    'via.Area': 'Area',
    'via.Torus': 'Torus',
    'via.Rect': 'Rect',
    'via.Rect3D': 'Rect3D',
    'via.Frustum': 'Frustum',
    'via.KeyFrame': 'KeyFrame',
    'Uri': 'Uri',
    'via.GameObjectRef': 'GameObjectRef',
    'via.Sfix': 'Sfix',
    'via.Sfix2': 'Sfix2',
    'via.Sfix3': 'Sfix3',
    'via.Sfix4': 'Sfix4',
    'via.Position': 'Position',
    'System.Decimal': 'Decimal',
}

TypeCode = [
    "Undefined",
    "Object",
    "Action",
    "Struct",
    "NativeObject",
    "Resource",
    "UserData",
    "Bool",
    "C8",
    "C16",
    "S8",
    "U8",
    "S16",
    "U16",
    "S32",
    "U32",
    "S64",
    "U64",
    "F32",
    "F64",
    "String",
    "MBString",
    "Enum",
    "Uint2",
    "Uint3",
    "Uint4",
    "Int2",
    "Int3",
    "Int4",
    "Float2",
    "Float3",
    "Float4",
    "Float3x3",
    "Float3x4",
    "Float4x3",
    "Float4x4",
    "Half2",
    "Half4",
    "Mat3",
    "Mat4",
    "Vec2",
    "Vec3",
    "Vec4",
    "VecU4",
    "Quaternion",
    "Guid",
    "Color",
    "DateTime",
    "AABB",
    "Capsule",
    "TaperedCapsule",
    "Cone",
    "Line",
    "LineSegment",
    "OBB",
    "Plane",
    "PlaneXZ",
    "Point",
    "Range",
    "RangeI",
    "Ray",
    "RayY",
    "Segment",
    "Size",
    "Sphere",
    "Triangle",
    "Cylinder",
    "Ellipsoid",
    "Area",
    "Torus",
    "Rect",
    "Rect3D",
    "Frustum",
    "KeyFrame",
    "Uri",
    "GameObjectRef",
    "RuntimeType",
    "Sfix",
    "Sfix2",
    "Sfix3",
    "Sfix4",
    "Position",
    "F16",
    "Decimal",
    "End",
]

TypeCodeSearch = dict([(k.lower(),v) for k,v in hardcoded_native_type_to_TypeCode.items()] + [(a.lower(), a) for a in TypeCode] + [("via."+a.lower(), a) for a in TypeCode] + [("system."+a.lower(), a) for a in TypeCode])
# print(TypeCodeSearch)

def generate_native_name(element, use_p_name, p, il2cpp_dump={}):
    if element is None:
        os.system("Error")

    if element["string"] == True:
        return "String"
    elif element["list"] == True:
        return generate_native_name(element["element"], use_p_name, p, il2cpp_dump)
    elif use_p_name:
        pt = p["type"]
        t = TypeCodeSearch.get(pt.lower(), "Data")
        # t = TypeCodeSearch.get(pt, "Data") if t=="Data" else t
        if t == "Data" and pt.startswith("via."):
            element = il2cpp_dump.get(pt, None)
            if element is None:
                return t
            parent = element.get('parent', None)
            if parent is not None:
                it = TypeCodeSearch.get(parent.lower(), "Data")
                # it = hardcoded_type_code_mapping.get(parent, "Data") if it=="Data" else it
                if it != 'Data':
                    return it
            chain = element.get('deserializer_chain', None)
            if chain is not None:
                for i in reversed(chain):
                    it = TypeCodeSearch.get(i['name'].lower(), "Data")
                    # it = hardcoded_type_code_mapping.get(i['name'], "Data") if it=="Data" else it
                    if it != 'Data':
                        return it
        return t
    return "Data"

def generate_field_entries(il2cpp_dump, natives, key, il2cpp_entry, use_typedefs, prefix = "", i=0, struct_i=0):
    e = il2cpp_entry
    parent_name = key

    fields_out = []
    struct_str = ""
    max_parent_level = 16

    # Go through parents until we run into a native that we need to insert at the top of the structure
    for f in range(0, max_parent_level):
        if natives is None or "parent" not in e:
            break

        if not (parent_name in il2cpp_dump and "RSZ" not in il2cpp_dump[parent_name] and parent_name in natives):
            # Keep going up the heirarchy of parents until we reach something usable
            if "parent" in e and e["parent"] in il2cpp_dump:
                parent_name = e["parent"]
                e = il2cpp_dump[e["parent"]]

            continue

        parent_native = natives[parent_name]
        found_anything = False

        for chain in parent_native:
            if "layout" not in chain or len(chain["layout"]) == 0:
                continue

            found_anything = True
            struct_str = struct_str + "// " + chain["name"] + " BEGIN\n"
            
            layout = chain["layout"]

            reflection_properties = il2cpp_dump[chain["name"]].get("reflection_properties", None)
            append_potential_name = False

            if len(layout) == len(reflection_properties):
                append_potential_name = True

                # sort reflection_properties by its native order
                order = [(int(v["order"]), (k,v)) for k, v in reflection_properties.items()]
                reflection_properties = dict([v for _, v in sorted(order)])

                for p, field in zip(reflection_properties.values(), layout):
                    t = hardcoded_native_type_to_TypeCode.get(p["type"].lower(), "Data")
                    if t == "Data":
                        pass
                    elif hardcoded_align_sizes[t]["align"] != field["align"]:
                        append_potential_name = False

            if append_potential_name:
                rp_names = list(reflection_properties.keys())
                rp_value = list(reflection_properties.values())
            else:
                rp_value = list(range(0, len(layout)))

            for rp_idx, field in enumerate(layout):
                native_type_name = generate_native_name(field, append_potential_name, rp_value[rp_idx], il2cpp_dump)
                native_field_name = "v" + str(i)
                native_org_type_name = ""
                if append_potential_name:
                    native_field_name += "_" + rp_names[rp_idx]
                    # native_field_name = rp_names[rp_idx] # without start with v_
                    native_org_type_name = rp_value[rp_idx]['type']
                    if native_type_name != "Data" and not native_org_type_name.startswith("via"):
                        native_org_type_name = "" # those would be sth like "bool" "s32"

                new_entry = {
                    "type": native_type_name,
                    "name": native_field_name,
                    "original_type": native_org_type_name,
                    "align": field["align"],
                    "size": field["size"],
                    "native": True
                }

                if "element" in field and "list" in field and field["list"] == True:
                    '''
                    new_entry["element"] = {
                        "type": generate_native_name(field["element"]),
                        "original_type": "",
                        "align": field["element"]["align"],
                        "size": field["element"]["size"],
                    }
                    '''
                    new_entry["align"] = field["element"]["align"]
                    new_entry["size"] = field["element"]["size"]
                    new_entry["array"] = True
                else:
                    new_entry["array"] = False

                fields_out.append(new_entry)

                struct_str = struct_str + "    " + native_type_name + " " + native_field_name + ";\n"
                i = i + 1

            struct_str = struct_str + "// " + chain["name"] + " END\n"
        
        if found_anything:
            break

    if "RSZ" in il2cpp_entry:
        for rsz_entry in il2cpp_entry["RSZ"]:
            name = "v" + str(i)

            if "potential_name" in rsz_entry:
                name = rsz_entry["potential_name"]

            code = rsz_entry["code"]
            type = rsz_entry["type"]

            # if code == "Struct" and type in il2cpp_dump:
            if False:
                nested_entry, nested_str, i, struct_i = generate_field_entries(il2cpp_dump, natives, type, il2cpp_dump[type], use_typedefs, "STRUCT_" + name + "_", i, struct_i)

                if len(nested_entry) > 0:
                    fields_out += nested_entry
                    struct_str = struct_str + nested_str
                    struct_i = struct_i + 1
            else:
                if code in hardcoded_align_sizes:
                    align_size = hardcoded_align_sizes[code]
                else:
                    align_size = als(rsz_entry["align"], int(rsz_entry["size"], 16))
                
                if use_typedefs == True:
                    if code in code_typedefs:
                        code = code_typedefs[code]
                    else:
                        code = "RSZ" + code

                '''
                if rsz_entry["array"] == True:
                    code = code + "List"
                '''

                fields_out.append({
                    "type": code,
                    "name": prefix + name,
                    "original_type": type,
                    "array": rsz_entry["array"] == 1,
                    "align": align_size["align"],
                    "size": align_size["size"],
                    "native": False
                })

                field_str = "    " + code + " " + name + "; //\"" + type + "\""
                struct_str = struct_str + field_str + "\n"
                
                i = i + 1
    
    return fields_out, struct_str, i, struct_i


def main(out_postfix="", il2cpp_path="", natives_path=None, use_typedefs=False, use_hashkeys=False):
    if il2cpp_path is None:
        return

    with open(il2cpp_path, "r", encoding="utf8") as f:
        il2cpp_dump = json.load(f)

    natives = None

    if natives_path is not None:
        with open(natives_path, "r", encoding="utf8") as f:
            natives = json.load(f)
    else:
        print("No natives file found, output may be incorrect for some types")

    out_str = ""
    out_json = {}

    for key, entry in il2cpp_dump.items():
        if entry is None:
            continue

        if use_hashkeys:
            out_json[entry["fqn"]] = {}
            json_entry = out_json[entry["fqn"]]
            json_entry["name"] = key
        else:
            out_json[key] = {}
            json_entry = out_json[key]
            json_entry["fqn"] = entry["fqn"]
        
        json_entry["crc"] = entry["crc"]

        if entry.get("is_generic_type", False):
            json_entry["element_type"] = [item["type"] for item in entry["generic_arg_types"]]
        elif entry.get("element_type_name", None) is not None:
            json_entry["element_type"] = [entry["element_type_name"]]
        else:
            json_entry["element_type"] = []

        struct_str = "// " + entry["fqn"] + "\n"
        struct_str = struct_str + "struct " + key + " {\n"

        fields, struct_body, _, __ = generate_field_entries(il2cpp_dump, natives, key, entry, use_typedefs)

        json_entry["fields"] = fields
        struct_str = struct_str + struct_body

        struct_str = struct_str + "};\n"
        out_str = out_str + struct_str

    with open("rsz" + out_postfix + ".txt", "w", encoding="utf8") as f:
        f.write(out_str)

    with open("rsz" + out_postfix + ".json", "w", encoding="utf8") as f:
        json.dump(out_json, f, indent='\t', sort_keys=True)


if __name__ == '__main__':
    fire.Fire(main)