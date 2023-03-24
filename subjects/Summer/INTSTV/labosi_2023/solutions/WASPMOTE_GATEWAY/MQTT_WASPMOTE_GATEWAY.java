
package mqtt;


import com.digi.xbee.api.exceptions.XBeeException;
import com.digi.xbee.api.listeners.IDataReceiveListener;
import com.digi.xbee.api.models.XBee64BitAddress;
import com.digi.xbee.api.models.XBeeMessage;
import com.digi.xbee.api.utils.HexUtils;
import com.digi.xbee.api.RemoteXBeeDevice;
import com.digi.xbee.api.XBeeDevice;
import com.digi.xbee.api.XBeeNetwork;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.MqttPersistenceException;
import org.eclipse.paho.client.mqttv3.MqttSecurityException;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;


class MyDataReceiveListener implements IDataReceiveListener {
	
	
	public void setXBeeDevice(XBeeDevice device) {
		myDevice = device;
	}

    static int QUALITY_OF_SERVICE = 2 ;
    
	static String _broker = "tcp://10.19.4.171:1883";
    
	static String clientId = "Test";
    
	static MemoryPersistence persistence = new MemoryPersistence();
    static MqttClient _client;
    
	
    static XBeeDevice _myDevice;
    
	static String topicHumidity = "mqtt/humidity";

    static String topicTemperature = "mqtt/temperature";

	static String topicAcceleration = "mqtt/acceleration";

	static String topicActuation = "topic/actuate";

	public void dataReceived(XBeeMessage xbeeMessage) {
		System.out.format("From %s >> %s | %s%n", xbeeMessage.getDevice().get64BitAddress(), 
				HexUtils.prettyHexString(HexUtils.byteArrayToHexString(xbeeMessage.getData())), 
				new String(xbeeMessage.getData()));
		
		String content = new String(xbeeMessage.getData());
		 try {
	            _client = new Mqtt_client(_broker, _clientId, persistence);
	            
	    String acceleration = getSensorValue(content, "ACC");
	    String temperature = getSensorValue(content, "TC");
	    String humidity = getSensorValue(content, "HUM");
	    
	            connectToMQTT();
	            
				setupMessageListenerCallback();
	            sendMessage(acceleration, topicAcceleration);
	            sendMessage(temperature, topicTemperature);
	            sendMessage(humidity, topicHumidity);

	            disconnectFromMQTT();	            
	            
	        } catch(MqttException ex) {

	            System.out.println("Reason "+ex.getReasonCode());
	            System.out.println("Message "ex.getMessage());
	            System.out.println("Location"+ex.getLocalizedMessage());
	            System.out.println("Cause of problem"+ex.getCause());
	            System.out.println("Exception "+ex);
	            
				ex.printStackTrace();
	        }
	}
	
	private static void setupMessageListenerCallback() {
  	  _client.setCallback(new MqttCallback() {

            public void connectionLost(Throwable cause)
			{
                System.out.println("connectionLost: " + cause.getMessage());
            }

            public void messageArrived(String topic, MqttMessage message) {
                System.out.println("Topic: " + topic);
                String content = new String(message.getPayload());
                System.out.println("Message content: " + content);
				RemoteXBeeDevice myRemoteXBeeDevice = new RemoteXBeeDevice(_myDevice, new XBee64BitAddress("0013A20040F8DC6D"));

				try
				{
					_myDevice.sendData(myRemoteXBeeDevice, content.getBytes());
				} catch (XBeeException e) 
				{					
					e.printStackTrace();
				}
           }

            public void deliveryComplete(IMqttDeliveryToken token) {
                System.out.println("I delivered message -->" + token.isComplete());
           }

       });
   }
	
	private static String getSensorValue(String inputString, String sensorName) {
		System.out.println("String from input is -->"+inputString);
        int startIndex = inputString.indexOf(sensorName) + sensorName.length() + 1;
        int endIndex = inputString.indexOf("#", startIndex);
        String valueString = inputString.substring(startIndex, endIndex);
        System.out.println("getSensorValue:"+valueString);
        return valueString;
    }
	  private static void connectToMQTT() {
	    	 MqttConnectOptions connOpts = new MqttConnectOptions();
	         connOpts.setCleanSession(true);
	         System.out.println("Connecting to _broker: "+_broker);
	         try {
				_client.connect(connOpts);
				_client.subscribe(topicActuation, QUALITY_OF_SERVICE);
			} catch (MqttSecurityException e) {
				e.printStackTrace();
			} catch (MqttException e) {
				e.printStackTrace();
			}
	         System.out.println("Connected from MQTT");
	    }
	    
	    private static void disconnectFromMQTT() {
	    	try {
				_client.disconnect();
			} catch (MqttException e) {
				e.printStackTrace();
			}
	        System.out.println("Disconnected from MQTT");
	    }
	    
	    private static void sendMessage(String message, String topic) {
	    	 MqttMessage msg = new MqttMessage(message.getBytes());
	         msg.setQUALITY_OF_SERVICE(QUALITY_OF_SERVICE);
	         try {
				_client.publish(topic, msg);
			} catch (MqttPersistenceException e) {
				e.printStackTrace();
			} catch (MqttException e) {
				e.printStackTrace();
			}
	         System.out.println("Message published");
	    }
}

public class XBeeGateway {
		
		private static final String PORT = "COM6";
		private static final int BAUD_RATE = 115200;

		
		public static void main(String[] args) {
			System.out.println(" +-----------------------------------------+");
			System.out.println(" |  XBee Java Library Receive Data Sample  |");
			System.out.println(" +-----------------------------------------+\n");
			
			XBeeDevice _myDevice = new XBeeDevice(PORT, BAUD_RATE);
			
			try {
				_myDevice.open();
				
				MyDataReceiveListener l = new MyDataReceiveListener();
				
				l.setXBeeDevice(_myDevice);
				
				_myDevice.addDataListener(l);				
							
				System.out.println("\n>> Waiting for data...");
				
			} catch (XBeeException e) {
				e.printStackTrace();
				System.exit(1);
			}
		}
		
	}