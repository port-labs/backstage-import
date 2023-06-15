import json
import requests
import os
import yaml 

BACKSTAGE_URL = os.environ.get("BACKSTAGE_URL")
API_URL = os.environ.get("API_URL")

if API_URL is None:
    API_URL = "https://api.getport.io/v1"

def get_required_headers():
    credentials = {'clientId': os.environ.get("PORT_CLIENT_ID"), 'clientSecret': os.environ.get("PORT_CLIENT_SECRET")}

    token_response = requests.post(f'{API_URL}/auth/access_token', json=credentials)

    access_token = token_response.json()['accessToken']
    return {
        'Authorization': f'Bearer {access_token}'
    }

def create_entity(blueprint, entity):
    print(f"Creating {blueprint} {entity['identifier']}")

    response = requests.post(
        f"{API_URL}/blueprints/{blueprint.lower()}/entities?create_missing_related_entities=true&upsert=true&merge=true",
        json=entity,
        headers=get_required_headers()
    )
    if response.status_code != 200:
        print(response.json())

    response.raise_for_status()

def parse_backstage_to_port_entity(backstage_entities):
    for backstage_entity in backstage_entities:
        blueprint = backstage_entity["kind"]
        identifier = backstage_entity["metadata"]["name"]
        description = backstage_entity["metadata"].get("description", "")
        labels = backstage_entity["metadata"].get("labels", {})
        
        annotations = backstage_entity.get("metadata", {}).get("annotations", {})
        title = backstage_entity.get("metadata", {}).get("title", identifier)
        tags = backstage_entity.get("metadata", {}).get("tags", [])
        links = map(lambda link: link.get("url", ""), backstage_entity.get("metadata", {}).get("links", []))

        entity = {
            "identifier": identifier,
            "title": title,
            "properties": {
                "description": description,
                "labels": labels,
                "annotations": annotations,
                "tags": tags,
                "links": list(links)
            },
            "relations": {
                
            }
        }

        if blueprint == "Group":
            type = backstage_entity.get("spec", {}).get("type", "")
            email = backstage_entity.get("spec", {}).get("profile", {}).get("email", None)
            parent = next(filter(lambda relation: relation["type"] == "childOf", backstage_entity["relations"]), None)
            members = list(filter(lambda relation: relation["type"] == "hasMember", backstage_entity["relations"]))
            entity["properties"]["type"] = type
            entity["properties"]["email"] = email

            entity["relations"]["parent"] = parent["target"]["name"] if parent else None
            entity["relations"]["members"] = list(map( lambda relation: relation["target"]["name"], members))
            create_entity(blueprint, entity)

        elif blueprint == "Component":
            type = backstage_entity.get("spec", {}).get("type", "")
            lifecycle = backstage_entity.get("spec", {}).get("lifecycle", "")

            owning_group = next(filter(lambda relation: relation["type"] == "ownedBy" and relation["target"]["kind"] == "group", backstage_entity["relations"]), None)
            owning_user = next(filter(lambda relation: relation["type"] == "ownedBy" and relation["target"]["kind"] == "user", backstage_entity["relations"]), None)
            system = next(filter(lambda relation: relation["type"] == "partOf" and relation["target"]["kind"] == "system", backstage_entity["relations"]), None)
            subcomponentOf = next(filter(lambda relation: relation["type"] == "partOf" and relation["target"]["kind"] == "component", backstage_entity["relations"]), None)
            providesApis = list(filter(lambda relation: relation["type"] == "providesApi", backstage_entity["relations"]))
            consumesApis = list(filter(lambda relation: relation["type"] == "consumesApi", backstage_entity["relations"]))
            dependsOnComponent = list(filter(lambda relation: relation["type"] == "dependsOn" and relation["target"]["kind"] == "component", backstage_entity["relations"]))
            dependsOnResource = list(filter(lambda relation: relation["type"] == "dependsOn" and relation["target"]["kind"] == "resource", backstage_entity["relations"]))

            entity["properties"]["type"] = type
            entity["properties"]["annotations"] = annotations
            entity["properties"]["lifecycle"] = lifecycle
            
            entity["relations"]["owningGroup"] = owning_group["target"]["name"] if owning_group else None
            entity["relations"]["owningUser"] = owning_user["target"]["name"] if owning_user else None
            entity["relations"]["system"] = system["target"]["name"] if system else None
            entity["relations"]["subcomponentOf"] = subcomponentOf["target"]["name"] if subcomponentOf else None
            entity["relations"]["providesApis"] = list(map( lambda relation: relation["target"]["name"], providesApis))
            entity["relations"]["consumesApis"] = list(map( lambda relation: relation["target"]["name"], consumesApis))
            entity["relations"]["dependsOnComponent"] = list(map( lambda relation: relation["target"]["name"], dependsOnComponent))
            entity["relations"]["dependsOnResource"] = list(map( lambda relation: relation["target"]["name"],dependsOnResource))
            create_entity(blueprint, entity)

        elif blueprint == "API":
            type = backstage_entity.get("spec", {}).get("type", "")
            lifecycle = backstage_entity.get("spec", {}).get("lifecycle", "")
            system = next(filter(lambda relation: relation["type"] == "partOf" and relation["target"]["kind"] == "system", backstage_entity["relations"]), None)
            owning_group = next(filter(lambda relation: relation["type"] == "ownedBy" and relation["target"]["kind"] == "group", backstage_entity["relations"]), None)
            owning_user = next(filter(lambda relation: relation["type"] == "ownedBy" and relation["target"]["kind"] == "user", backstage_entity["relations"]), None)
            definitionOpenAPI = None
            definitionAsyncAPI = None
            definitionGraphQL = None
            definitionGRPC = None

            if type == "openapi":
                definitionOpenAPI = json.loads(json.dumps(yaml.load(backstage_entity.get("spec", {}).get("definition", ""), Loader=yaml.SafeLoader), indent=4, sort_keys=True, default=str))
            elif type == "asyncapi":
                definitionAsyncAPI = json.loads(json.dumps(yaml.load(backstage_entity.get("spec", {}).get("definition", ""), Loader=yaml.SafeLoader), indent=4, sort_keys=True, default=str))
            elif type == "graphql":
                definitionGraphQL = backstage_entity.get("spec", {}).get("definition", "")
            elif type == "grpc":
                definitionGRPC = backstage_entity.get("spec", {}).get("definition", "")

            entity["properties"]["type"] = type
            entity["properties"]["lifecycle"] = lifecycle
            entity["properties"]["definitionOpenAPI"] = definitionOpenAPI if definitionOpenAPI else None
            entity["properties"]["definitionAsyncAPI"] = definitionAsyncAPI if definitionAsyncAPI else None
            entity["properties"]["definitionGraphQL"] = definitionGraphQL if definitionGraphQL else None
            entity["properties"]["definitionGRPC"] = definitionGRPC if definitionGRPC else None
            entity["relations"]["system"] = system["target"]["name"] if system else None
            entity["relations"]["owningGroup"] = owning_group["target"]["name"] if owning_group else None
            entity["relations"]["owningUser"] = owning_user["target"]["name"] if owning_user else None
            create_entity(blueprint, entity)

        elif blueprint == "User":
            email = backstage_entity.get("spec", {}).get("profile", {}).get("email", None)
            entity["properties"]["email"] = email
            create_entity(blueprint, entity)

        elif blueprint == "Resource":
            type = backstage_entity.get("spec", {}).get("type", "")
            
            system = next(filter(lambda relation: relation["type"] == "partOf" and relation["target"]["kind"] == "system", backstage_entity["relations"]), None)
            owning_group = next(filter(lambda relation: relation["type"] == "ownedBy" and relation["target"]["kind"] == "group", backstage_entity["relations"]), None)
            owning_user = next(filter(lambda relation: relation["type"] == "ownedBy" and relation["target"]["kind"] == "user", backstage_entity["relations"]), None)
            dependsOnResource = list(filter(lambda relation: relation["type"] == "dependsOn" and relation["target"]["kind"] == "resource", backstage_entity["relations"]))
            dependsOnComponent = list(filter(lambda relation: relation["type"] == "dependsOn" and relation["target"]["kind"] == "component", backstage_entity["relations"]))
            entity["properties"]["type"] = type
            entity["relations"]["owningGroup"] = owning_group["target"]["name"] if owning_group else None
            entity["relations"]["owningUser"] = owning_user["target"]["name"] if owning_user else None
            entity["relations"]["system"] = system["target"]["name"] if system else None
            entity["relations"]["dependsOnResource"] = list(map( lambda relation: relation["target"]["name"],dependsOnResource))
            entity["relations"]["dependsOnComponent"] = list(map( lambda relation: relation["target"]["name"],dependsOnComponent))
            create_entity(blueprint, entity)
        
        elif blueprint == "System":
            type = backstage_entity.get("spec", {}).get("type", "")
            owning_user = next(filter(lambda relation: relation["type"] == "ownedBy" and relation["target"]["kind"] == "user", backstage_entity["relations"]), None)
            owning_group = next(filter(lambda relation: relation["type"] == "ownedBy" and relation["target"]["kind"] == "group", backstage_entity["relations"]), None)
            domain = next(filter(lambda relation: relation["type"] == "partOf", backstage_entity["relations"]), None)

            entity["properties"]["type"] = type
            entity["relations"]["owningUser"] = owning_user["target"]["name"] if owning_user else None
            entity["relations"]["owningGroup"] = owning_group["target"]["name"] if owning_group else None
            entity["relations"]["domain"] = domain["target"]["name"] if domain else None
            create_entity(blueprint, entity)
        
        elif blueprint == "Domain":
            owning_user = next(filter(lambda relation: relation["type"] == "ownedBy" and relation["target"]["kind"] == "user", backstage_entity["relations"]), None)
            owning_group = next(filter(lambda relation: relation["type"] == "ownedBy" and relation["target"]["kind"] == "group", backstage_entity["relations"]), None)

            entity["relations"]["owningUser"] = owning_user["target"]["name"] if owning_user else None
            entity["relations"]["owningGroup"] = owning_group["target"]["name"] if owning_group else None
            create_entity(blueprint, entity)

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
            
            response = requests.post(f"{API_URL}/blueprints", json=blueprint, headers=get_required_headers())

            if response.status_code >= 400 and response.status_code != 409:
                response.raise_for_status()
            
        # Update blueprint with relation
        for blueprint in blueprints:
            print(f"Upserting relations for blueprint {blueprint.get('identifier')}")

            response = requests.put(f"{API_URL}/blueprints/{blueprint.get('identifier')}", json=blueprint, headers=get_required_headers())
            response.raise_for_status()


if __name__ == "__main__":
    upsert_blueprints_from_json('blueprints.json')

    response = requests.get(f"{BACKSTAGE_URL}/api/catalog/entities")
    response.raise_for_status()
    
    parse_backstage_to_port_entity(response.json())

