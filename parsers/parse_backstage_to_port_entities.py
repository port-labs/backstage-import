
import json

import yaml


def parse_backstage_to_port_entities(backstage_entities):
    port_entities = []
    supported_kinds = ["Group", "Component",
                       "System", "API", "Resource", "User", "Domain"]

    for backstage_entity in backstage_entities:
        blueprint = backstage_entity["kind"]
        identifier = backstage_entity["metadata"]["name"]
        description = backstage_entity["metadata"].get("description", "")
        labels = backstage_entity["metadata"].get("labels", {})

        annotations = backstage_entity.get(
            "metadata", {}).get("annotations", {})
        title = backstage_entity.get("metadata", {}).get("title", identifier)
        tags = backstage_entity.get("metadata", {}).get("tags", [])
        links = map(lambda link: link.get("url", ""),
                    backstage_entity.get("metadata", {}).get("links", []))

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
            email = backstage_entity.get("spec", {}).get(
                "profile", {}).get("email", None)
            parent = next(filter(
                lambda relation: relation["type"] == "childOf", backstage_entity["relations"]), None)
            members = list(filter(
                lambda relation: relation["type"] == "hasMember", backstage_entity["relations"]))
            entity["properties"]["type"] = type
            entity["properties"]["email"] = email

            entity["relations"]["parent"] = parent["target"]["name"] if parent else None
            entity["relations"]["members"] = list(
                map(lambda relation: relation["target"]["name"], members))

        elif blueprint == "Component":
            type = backstage_entity.get("spec", {}).get("type", "")
            lifecycle = backstage_entity.get("spec", {}).get("lifecycle", "")

            owning_group = next(filter(
                lambda relation: relation["type"] == "ownedBy" and relation["target"]["kind"] == "group", backstage_entity["relations"]), None)
            owning_user = next(filter(
                lambda relation: relation["type"] == "ownedBy" and relation["target"]["kind"] == "user", backstage_entity["relations"]), None)
            system = next(filter(
                lambda relation: relation["type"] == "partOf" and relation["target"]["kind"] == "system", backstage_entity["relations"]), None)
            subcomponentOf = next(filter(
                lambda relation: relation["type"] == "partOf" and relation["target"]["kind"] == "component", backstage_entity["relations"]), None)
            providesApis = list(filter(
                lambda relation: relation["type"] == "providesApi", backstage_entity["relations"]))
            consumesApis = list(filter(
                lambda relation: relation["type"] == "consumesApi", backstage_entity["relations"]))
            dependsOnComponent = list(filter(
                lambda relation: relation["type"] == "dependsOn" and relation["target"]["kind"] == "component", backstage_entity["relations"]))
            dependsOnResource = list(filter(
                lambda relation: relation["type"] == "dependsOn" and relation["target"]["kind"] == "resource", backstage_entity["relations"]))

            entity["properties"]["type"] = type
            entity["properties"]["annotations"] = annotations
            entity["properties"]["lifecycle"] = lifecycle

            entity["relations"]["owningGroup"] = owning_group["target"]["name"] if owning_group else None
            entity["relations"]["owningUser"] = owning_user["target"]["name"] if owning_user else None
            entity["relations"]["system"] = system["target"]["name"] if system else None
            entity["relations"]["subcomponentOf"] = subcomponentOf["target"]["name"] if subcomponentOf else None
            entity["relations"]["providesApis"] = list(
                map(lambda relation: relation["target"]["name"], providesApis))
            entity["relations"]["consumesApis"] = list(
                map(lambda relation: relation["target"]["name"], consumesApis))
            entity["relations"]["dependsOnComponent"] = list(
                map(lambda relation: relation["target"]["name"], dependsOnComponent))
            entity["relations"]["dependsOnResource"] = list(
                map(lambda relation: relation["target"]["name"], dependsOnResource))

        elif blueprint == "API":
            type = backstage_entity.get("spec", {}).get("type", "")
            lifecycle = backstage_entity.get("spec", {}).get("lifecycle", "")
            system = next(filter(
                lambda relation: relation["type"] == "partOf" and relation["target"]["kind"] == "system", backstage_entity["relations"]), None)
            owning_group = next(filter(
                lambda relation: relation["type"] == "ownedBy" and relation["target"]["kind"] == "group", backstage_entity["relations"]), None)
            owning_user = next(filter(
                lambda relation: relation["type"] == "ownedBy" and relation["target"]["kind"] == "user", backstage_entity["relations"]), None)
            definitionOpenAPI = None
            definitionAsyncAPI = None
            definitionGraphQL = None
            definitionGRPC = None

            if type == "openapi":
                definitionOpenAPI = json.loads(json.dumps(yaml.load(backstage_entity.get("spec", {}).get(
                    "definition", ""), Loader=yaml.SafeLoader), indent=4, sort_keys=True, default=str))
            elif type == "asyncapi":
                definitionAsyncAPI = json.loads(json.dumps(yaml.load(backstage_entity.get("spec", {}).get(
                    "definition", ""), Loader=yaml.SafeLoader), indent=4, sort_keys=True, default=str))
            elif type == "graphql":
                definitionGraphQL = backstage_entity.get(
                    "spec", {}).get("definition", "")
            elif type == "grpc":
                definitionGRPC = backstage_entity.get(
                    "spec", {}).get("definition", "")

            entity["properties"]["type"] = type
            entity["properties"]["lifecycle"] = lifecycle
            entity["properties"]["definitionOpenAPI"] = definitionOpenAPI if definitionOpenAPI else None
            entity["properties"]["definitionAsyncAPI"] = definitionAsyncAPI if definitionAsyncAPI else None
            entity["properties"]["definitionGraphQL"] = definitionGraphQL if definitionGraphQL else None
            entity["properties"]["definitionGRPC"] = definitionGRPC if definitionGRPC else None
            entity["relations"]["system"] = system["target"]["name"] if system else None
            entity["relations"]["owningGroup"] = owning_group["target"]["name"] if owning_group else None
            entity["relations"]["owningUser"] = owning_user["target"]["name"] if owning_user else None

        elif blueprint == "User":
            email = backstage_entity.get("spec", {}).get(
                "profile", {}).get("email", None)
            entity["properties"]["email"] = email

        elif blueprint == "Resource":
            type = backstage_entity.get("spec", {}).get("type", "")

            system = next(filter(
                lambda relation: relation["type"] == "partOf" and relation["target"]["kind"] == "system", backstage_entity["relations"]), None)
            owning_group = next(filter(
                lambda relation: relation["type"] == "ownedBy" and relation["target"]["kind"] == "group", backstage_entity["relations"]), None)
            owning_user = next(filter(
                lambda relation: relation["type"] == "ownedBy" and relation["target"]["kind"] == "user", backstage_entity["relations"]), None)
            dependsOnResource = list(filter(
                lambda relation: relation["type"] == "dependsOn" and relation["target"]["kind"] == "resource", backstage_entity["relations"]))
            dependsOnComponent = list(filter(
                lambda relation: relation["type"] == "dependsOn" and relation["target"]["kind"] == "component", backstage_entity["relations"]))
            entity["properties"]["type"] = type
            entity["relations"]["owningGroup"] = owning_group["target"]["name"] if owning_group else None
            entity["relations"]["owningUser"] = owning_user["target"]["name"] if owning_user else None
            entity["relations"]["system"] = system["target"]["name"] if system else None
            entity["relations"]["dependsOnResource"] = list(
                map(lambda relation: relation["target"]["name"], dependsOnResource))
            entity["relations"]["dependsOnComponent"] = list(
                map(lambda relation: relation["target"]["name"], dependsOnComponent))

        elif blueprint == "System":
            type = backstage_entity.get("spec", {}).get("type", "")
            owning_user = next(filter(
                lambda relation: relation["type"] == "ownedBy" and relation["target"]["kind"] == "user", backstage_entity["relations"]), None)
            owning_group = next(filter(
                lambda relation: relation["type"] == "ownedBy" and relation["target"]["kind"] == "group", backstage_entity["relations"]), None)
            domain = next(filter(
                lambda relation: relation["type"] == "partOf", backstage_entity["relations"]), None)

            entity["properties"]["type"] = type
            entity["relations"]["owningUser"] = owning_user["target"]["name"] if owning_user else None
            entity["relations"]["owningGroup"] = owning_group["target"]["name"] if owning_group else None
            entity["relations"]["domain"] = domain["target"]["name"] if domain else None

        elif blueprint == "Domain":
            owning_user = next(filter(
                lambda relation: relation["type"] == "ownedBy" and relation["target"]["kind"] == "user", backstage_entity["relations"]), None)
            owning_group = next(filter(
                lambda relation: relation["type"] == "ownedBy" and relation["target"]["kind"] == "group", backstage_entity["relations"]), None)

            entity["relations"]["owningUser"] = owning_user["target"]["name"] if owning_user else None
            entity["relations"]["owningGroup"] = owning_group["target"]["name"] if owning_group else None

        if blueprint in supported_kinds:
            port_entities.append(
                {"blueprint": blueprint.lower() if blueprint != "API" else blueprint, "entity": entity})

    return port_entities
