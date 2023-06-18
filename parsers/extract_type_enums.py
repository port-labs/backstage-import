def extract_type_enums(port_entities):
    type_to_enums_per_blueprint = {}

    for entity_and_blueprint in port_entities:
        entity = entity_and_blueprint["entity"]
        blueprint = entity_and_blueprint["blueprint"]

        if blueprint not in type_to_enums_per_blueprint:
            type_to_enums_per_blueprint[blueprint] = []

        if "type" in entity["properties"]:
            if entity["properties"]["type"] not in type_to_enums_per_blueprint[blueprint]:
                type_to_enums_per_blueprint[blueprint].append(
                    entity["properties"]["type"])

    return type_to_enums_per_blueprint
