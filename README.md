## Multi-Container Service with RabbitMQ and CSV

### Description
This is a multi-container service that consists of a producer, a RabbitMQ container, and a consumer. The producer is a simple web-service that accepts a POST request with a JSON body, validates the body, parses and pushes the message to the RabbitMQ queue. The consumer consumes the RabbitMQ queue for messages, transforms the message, and appends it into a CSV file.

### Usage
To run the service, first make sure that you have Docker and Docker Compose installed on your system. Then follow the steps below:

1. Clone the repository:
   ```
   $ git clone https://github.com/<your_username>/multi-container-service.git
   ```
2. Navigate to the project directory:
   ```
   $ cd multi-container-service
   ```
3. Build the Docker images:
   ```
   $ docker-compose build
   ```
4. Start the Docker containers:
   ```
   $ docker-compose up -d
   ```
   This will start three containers - a producer, a RabbitMQ container, and a consumer. The producer will be accessible at http://localhost:8000.

5. To test the service, you can use the sample request provided in the prompt:
   ```
   POST
   {
       "device_id": str,
       "client_id": str,
       "created_at": str, # timestamp, e.g. '2023-02-07 14:56:49.386042'
       "data": {
           "license_id": str,
           "preds": [
               {
                   "image_frame": str, # base64 string
                   "prob": float,
                   "tags": str[]
               },
               ...
           ] 
       }
   }
   ```
   You can send a request using curl:
   ```
   $ curl -X POST -H "Content-Type: application/json" \
          -d '{"device_id":"1234", "client_id":"5678", "created_at":"2023-04-21 10:30:00", "data":{"license_id":"ABCD-1234", "preds":[{"image_frame":"<base64_string>", "prob":0.8, "tags":["car", "red"]}]}}' \
          http://localhost:8000
   ```
6. The output CSV file will be generated in the output directory of the consumer container. You can copy it to your local machine using the docker cp command:
   ```
   $ docker cp multi-container-service_consumer_1:/output/predictions.csv ./predictions.csv
   ```

### Configuration
The service can be configured using environment variables. The following variables are available:

- PRODUCER_HOST: The hostname of the producer container. Default is producer.
- PRODUCER_PORT: The port number of the producer container. Default is 8000.
- RABBITMQ_HOST: The hostname of the RabbitMQ container. Default is rabbitmq.
- RABBITMQ_PORT: The port number of the RabbitMQ container. Default is 5672.
- RABBITMQ_QUEUE: The name of the RabbitMQ queue. Default is predictions.
- OUTPUT_FILE: The name of the output CSV file. Default is predictions.csv.

You can set these variables in the docker-compose.yml file or in a .env file in the project directory.