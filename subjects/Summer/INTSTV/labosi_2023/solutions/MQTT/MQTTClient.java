import org.eclipse.paho.client.mqttv3.*;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;

public class MQTTClient {

	private static String brokerAddress = "tcp://10.129.5.176:1883";
	private static String clientName = "Test";

	private static String temperature = "mqtt/temperature";
	private static String humidity = "mqtt/humidity";
	private static String acceleration = "mqtt/acceleration";
	private static String actuationOutput = "topic/actuate";    

	private static MqttClient _client;
	
	private static MqttConnectOptions options = new MqttConnectOptions();

	private static int QUALITY_OF_SERVICE = 2;
	
	private static int interval = 230;

	public static void main(String[] args) {
		try {
			_client = new Mqtt_client(brokerAddress, _clientName, new MemoryPersistence());
			clientCONNECT();
			
			topicsSUBSCRIBE();
			
		} catch (Exception e) {
			
			e.printStackTrace();
			
		}
		
	}

	private static void clientCONNECT() {
		
		options = new MqttConnectOptions();		
		options.setConnectionTimeout(interval);
		options.setKeepAliveInterval(interval);
		

		try {
			_client.connect(options);
		} catch (Exception e) {
			
			e.printStackTrace();
			
			
		}
		
		MqttCallback callback = new MqttCallback() {

			public void connectionLost(Throwable cause) {
				
				System.out.println("Connection interrupted for --> " + cause.getMessage());
				
			}

			public void messageArrived(String topic, MqttMessage message) {
				String value = new String(message.getPayload());
				
				System.out.println(" I got message: " + value + " in topic: " + topic);
				
				if (Float.parseFloat(value) != 1) return;
				
				System.out.println("Message was sent");

				sendMessage(value, actuationOutput);
			}

			public void deliveryComplete(IMqttDeliveryToken token) {
				System.out.println("manged to deliver " + token.isComplete());
			}
		};
		
		_client.setCallback(callback);

	}
	
	private static void topicsSUBSCRIBE() {
		try {
			_client.subscribe(temperature, QUALITY_OF_SERVICE);
			_client.subscribe(acceleration, QUALITY_OF_SERVICE);
			_client.subscribe(humidity, QUALITY_OF_SERVICE);
		} catch (Exception e) 
		{			
			e.printStackTrace();		
		}
	}

	private static void sendMsgToTopic(String payload, String topic) {
		
		MqttMessage message = new MqttMessage(payload.getBytes());
		message.setQUALITY_OF_SERVICE(QUALITY_OF_SERVICE);
		
		try {
			_client.publish(topic, message);
		} 
		catch (Exception e) 
		{
			e.printStackTrace();
		} 
	}
	
}
