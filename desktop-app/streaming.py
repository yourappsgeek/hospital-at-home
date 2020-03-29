
from google.cloud import pubsub_v1



def get_callback(api_future, message_id):
    """Wrap message data in the context of the callback function."""
    def callback(api_future):
        try:
            print("Published message {} now has event ID {}".format(
                message_id, api_future.result()))
        except Exception:
            print("A problem occurred when publishing {}: {}\n".format(
                message_id, api_future.exception()))
            raise
    return callback


def publish(project_id, topic_name, message):
    """Publishes a message to a Pub/Sub topic.
    Args:
        project_id (str): Google Cloud Project ID
        topic_name (str): Pub/Sub topic name
        message (dict): Message dictionary
    """
    # Initialize a Publisher client
    client = pubsub_v1.PublisherClient()
    topic_path = client.topic_path(project_id, topic_name)

    # publish the message
    api_future = client.publish(
        topic_path, **message
    )

    api_future.add_done_callback(get_callback(api_future, message['message_id']))



