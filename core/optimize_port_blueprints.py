
import json
from clients.port_client.blueprint import update_blueprint
from parsers.extract_relations_in_use import extract_relations_in_use
from parsers.extract_type_enums import extract_type_enums


def optimize_port_blueprints(port_entities, file):
    print("Optimizing port blueprints")

    relations_in_use_per_blueprint = extract_relations_in_use(port_entities)
    type_to_enums_per_blueprint = extract_type_enums(port_entities)

    with open(file) as json_file:
        blueprints = json.load(json_file)

        for blueprint in blueprints:
            blueprint_relations = blueprint.get("relations", {}).keys()
            blueprint_relations_in_use = relations_in_use_per_blueprint.get(
                blueprint.get('identifier'), [])
            blueprint_relation_not_in_use = list(filter(
                lambda relation: relation not in blueprint_relations_in_use, blueprint_relations))

            # optimize un used relations
            for relation in blueprint_relation_not_in_use:
                del blueprint["relations"][relation]

            # optimize types to enums

            if "type" in blueprint.get("schema", {}).get("properties", {}):
                blueprint_type_enum = type_to_enums_per_blueprint.get(
                    blueprint.get('identifier'), [])
                if len(blueprint_type_enum) > 0:
                    blueprint["schema"]["properties"]["type"]["enum"] = blueprint_type_enum

            update_blueprint(blueprint)
