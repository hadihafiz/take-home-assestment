import pika
import csv

def callback(ch, method, properties, body):
    """
    Callback function to consume messages from the RabbitMQ queue.

    Param ch: Channel object
    Param method: Method object
    Param properties: Properties object
    Param body: Message body
    """
    message = body.decode('utf-8')
    headers = [key for key in json.loads(message).keys()]
    preds = json.loads(message)['data']['preds']
    with open('/output/predictions.csv', mode='a') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(headers)
        for pred in preds:
            row = [json.loads(message)[key] if key != 'preds' else pred[key] for key in headers]
            writer.writerow(row)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def consume_messages():
    """
    Consume messages from the RabbitMQ queue.
    """
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        channel = connection.channel()
        channel.queue_declare(queue='predictions')
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue='predictions', on_message_callback=callback)
        channel.start_consuming()
    except:
        pass

if __name__ == '__main__':
    # Example
    consume_messages()