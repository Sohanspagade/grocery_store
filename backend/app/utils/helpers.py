from bson import ObjectId

def serialize_dict(a_dict) -> dict:
    return {**{i: str(a_dict[i]) for i in a_dict if isinstance(a_dict[i], ObjectId)},
            **{i: a_dict[i] for i in a_dict if not isinstance(a_dict[i], ObjectId)}}

def serialize_list(entity) -> list:
    return [serialize_dict(a) for a in entity]
