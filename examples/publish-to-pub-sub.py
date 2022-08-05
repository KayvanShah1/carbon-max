from datetime import datetime
import json
import random
import uuid
from google.cloud import pubsub_v1

project_id = "optical-unison-356814"
topic_id = "test-topic"

publisher_options = pubsub_v1.types.PublisherOptions(enable_message_ordering=True)
# Sending messages to the same region ensures they are received in order
# even when multiple publishers are used.
client_options = {"api_endpoint": "us-east1-pubsub.googleapis.com:443"}
publisher = pubsub_v1.PublisherClient(
    publisher_options=publisher_options, client_options=client_options
)
# The `topic_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/topics/{topic_id}`
topic_path = publisher.topic_path(project_id, topic_id)

message = {
    "glossary": {
        "title": "example glossary",
        "GlossDiv": {
            "title": "S",
            "GlossList": {
                "GlossEntry": {
                    "ID": "SGML",
                    "SortAs": "SGML",
                    "GlossTerm": "Standard Generalized Markup Language",
                    "Acronym": "SGML",
                    "Abbrev": "ISO 8879:1986",
                    "GlossDef": {
                        "para": "A meta-markup language, used to create markup languages such as DocBook.",
                        "GlossSeeAlso": ["GML", "XML"],
                    },
                    "GlossSee": "markup",
                }
            },
        },
    }
}


def get_key(num_keys):
    key_list = [i + 1 for i in range(num_keys)]
    number = random.choice(key_list)
    return f"key{number}"


for num_messages in range(10):
    # Data must be a bytestring
    message["glossary"]["id"] = str(uuid.uuid4())
    message["glossary"]["publish_datetime"] = str(datetime.now())
    message_tuple = (json.dumps(message), get_key(4))
    data = message_tuple[0].encode("utf-8")
    ordering_key = message_tuple[1]

    # When you publish a message, the client returns a future.
    future = publisher.publish(topic_path, data=data, ordering_key=ordering_key)
    print(future.result())

print(f"Published messages with ordering keys to {topic_path}.")
