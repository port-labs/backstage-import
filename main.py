import os
import concurrent.futures

from clients.backstage_client.entity import get_backstage_entities
from clients.port_client.entity import create_entity
from core.optimize_port_blueprints import optimize_port_blueprints
from core.upsert_blueprints_from_json_file import upsert_blueprints_from_json
from parsers.parse_backstage_to_port_entities import parse_backstage_to_port_entities

MAX_CONCURRENCY = int(os.getenv("MAX_CONCURRENCY", "1"))

def create_entity_concurrent(blueprint, entity):
    create_entity(blueprint, entity)

if __name__ == "__main__":
    file_location = os.path.join(os.path.dirname(__file__), 'blueprints.json')

    upsert_blueprints_from_json(file_location)

    backstage_entities = get_backstage_entities()
    port_entities = parse_backstage_to_port_entities(backstage_entities)

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_CONCURRENCY) as executor:
        futures = [executor.submit(create_entity_concurrent, entity_and_blueprint["blueprint"], entity_and_blueprint["entity"]) for entity_and_blueprint in port_entities]
        concurrent.futures.wait(futures)

    optimize_port_blueprints(port_entities, file_location)
