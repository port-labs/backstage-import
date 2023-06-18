import os

from clients.backstage_client.entity import get_backstage_entities
from clients.port_client.entity import create_entity
from core.optimize_port_blueprints import optimize_port_blueprints
from core.upsert_blueprints_from_json_file import upsert_blueprints_from_json
from parsers.parse_backstage_to_port_entities import parse_backstage_to_port_entities


if __name__ == "__main__":
    file_location = os.path.join(os.path.dirname(__file__), 'blueprints.json')

    upsert_blueprints_from_json(file_location)

    backstage_entities = get_backstage_entities()
    port_entities = parse_backstage_to_port_entities(backstage_entities)

    for entity_and_blueprint in port_entities:
        entity = entity_and_blueprint["entity"]
        blueprint = entity_and_blueprint["blueprint"]

        create_entity(blueprint, entity)

    optimize_port_blueprints(port_entities, file_location)
