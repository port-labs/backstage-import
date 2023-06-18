import json

from clients.port_client.blueprint import create_blueprint, update_blueprint


def upsert_blueprints_from_json(file):
    print(f"Upserting blueprints from {file}")

    with open(file) as json_file:
        blueprints = json.load(json_file)

        # Upsert blueprints without relations
        for blueprint in blueprints:
            blueprint = blueprint.copy()
            print(f"Upserting blueprint {blueprint.get('identifier')}")
            # Remove the "relation" key from the blueprint
            if "relations" in blueprint:
                del blueprint["relations"]

            create_blueprint(blueprint)

        for blueprint in blueprints:
            print(
                f"Upserting relations for blueprint {blueprint.get('identifier')}")

            update_blueprint(blueprint)
