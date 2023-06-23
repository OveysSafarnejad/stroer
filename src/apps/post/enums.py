from apps.core.structs import EnumBase, EnumMember


class ActionEnum(EnumBase):
    CREATE = EnumMember(0, "Create")
    UPDATE = EnumMember(1, "Update")
    DELETE = EnumMember(2, "Delete")
