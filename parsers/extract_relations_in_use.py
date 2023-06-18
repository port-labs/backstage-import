def extract_relations_in_use(port_entities):
    relations_in_use_per_blueprint = {}

    for entity_and_blueprint in port_entities:
        entity = entity_and_blueprint["entity"]
        blueprint = entity_and_blueprint["blueprint"]

        for relation in entity["relations"].keys():
            if blueprint not in relations_in_use_per_blueprint:
                relations_in_use_per_blueprint[blueprint] = []

            if relation not in relations_in_use_per_blueprint[blueprint]:
                if isinstance(entity["relations"][relation], list):
                    if len(entity["relations"][relation]) > 0:
                        relations_in_use_per_blueprint[blueprint].append(
                            relation)
                else:
                    if entity["relations"][relation] is not None:
                        relations_in_use_per_blueprint[blueprint].append(
                            relation)

    return relations_in_use_per_blueprint
