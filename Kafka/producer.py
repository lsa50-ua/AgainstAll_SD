from kafka import KafkaProducer
import msvcrt

bootstrap_servers = ['localhost:9092']
topicName = 'SD'
producer = KafkaProducer(bootstrap_servers = bootstrap_servers)
producer = KafkaProducer()

print("pulsa ESC para parar la ejecucion")
while 1:
    if msvcrt.kbhit():
        msg = msvcrt.getch()
        #la tecla 27 es el ESC
        if ord(msg) != 27:
            ack = producer.send(topicName, msg)
            print("Enviando msg:", msg.decode('utf-8'))
            #metadata = ack.get()
        else:
            break


#print(metadata.topic)
#print(metadata.partition)

#If you want to set some more properties for your Producer or change its serialization format you can use the following lines of code:
    #producer = KafkaProducer(bootstrap_servers = bootstrap_servers, retries = 5,value_serializer=lambda m: json.dumps(m).encode('ascii'))
