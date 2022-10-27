from kafka import KafkaProducer

bootstrap_servers = ['localhost:9092']
topicName = 'myTopic'
producer = KafkaProducer(bootstrap_servers = bootstrap_servers)
producer = KafkaProducer()

ack = producer.send(topicName, b'Hello World!!!!!!!!')
metadata = ack.get()

print(metadata.topic)
print(metadata.partition)

#If you want to set some more properties for your Producer or change its serialization format you can use the following lines of code:
    #producer = KafkaProducer(bootstrap_servers = bootstrap_servers, retries = 5,value_serializer=lambda m: json.dumps(m).encode('ascii'))
