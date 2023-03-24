/*
    ------ Waspmote Pro Code Example --------

    Explanation: This is the basic Code for Waspmote Pro

    Copyright (C) 2016 Libelium Comunicaciones Distribuidas S.L.
    http://www.libelium.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/


#include <WaspXBeeZB.h>
#include <WaspFrame.h>
#include <WaspSensorEvent_v30.h>

float humid;
float acc;
float temp;
uint8_t dest[8];

char GW_ADDRESS[] = "0013A200414EA7EC";
char ED_ADDRESS[] = "0013A20040F8DC4A";
char RX_ADDRESS[] = "0013A20040F8DBFD";

uint8_t error;
uint8_t  PANID[8] = {0x33, 0x44, 0x55, 0x66, 0x77, 0x88, 0x99, 0x11};
uint8_t macED1_lastHEX = 0x4A;
uint8_t macGW_lastHEX = 0xEC;

void setup()
{
  USB.ON();
  xbeeZB.ON();

  ///////////////////////////////////////////////
  // 1. Disable Coordinator mode
  ///////////////////////////////////////////////

  xbeeZB.setCoordinator(DISABLED);

  // check at command flag
  if (xbeeZB.error_AT == 0)
  {
    USB.println(F("1. Coordinator mode disabled"));
  }
  else
  {
    USB.println(F("1. Error while disabling Coordinator mode"));
  }

  ///////////////////////////////////////////////
  // 2. Set PANID
  ///////////////////////////////////////////////
  xbeeZB.setPAN(PANID);

  // check at command flag
  if (xbeeZB.error_AT == 0)
  {
    USB.println(F("2. PANID set OK"));
  }
  else
  {
    USB.println(F("2. Error while setting PANID"));
  }

  ///////////////////////////////////////////////
  // 3. Set channels to be scanned before creating network
  ///////////////////////////////////////////////
  // channels from 0x0B to 0x18 (0x19 and 0x1A are excluded)
  /* Range:[0x0 to 0x3FFF]
    Channels are scpedified as a bitmap where depending on
    the bit a channel is selected --> Bit (Channel):
     0 (0x0B)  4 (0x0F)  8 (0x13)   12 (0x17)
     1 (0x0C)  5 (0x10)  9 (0x14)   13 (0x18)
     2 (0x0D)  6 (0x11)  10 (0x15)
     3 (0x0E)  7 (0x12)   11 (0x16)    */
  xbeeZB.setScanningChannels(0x00, 0x01);

  // check at command flag
  if (xbeeZB.error_AT == 0)
  {
    USB.println(F("3. Scanning channels set OK"));
  }
  else
  {
    USB.println(F("3. Error while setting 'Scanning channels'"));
  }
  
  ///////////////////////////////////////////////
  // Save values
  ///////////////////////////////////////////////
  xbeeZB.writeValues();

  // wait for the module to set the parameters
  delay(10000);
  USB.println();

  
  // 1. get operating 64-b PAN ID
  xbeeZB.getOperating64PAN();

  // 2. wait for association indication
  xbeeZB.getAssociationIndication();
 
  while( xbeeZB.associationIndication != 0 )
  { 
    delay(2000);
    
    // get operating 64-b PAN ID
    xbeeZB.getOperating64PAN();

    USB.print(F("operating 64-b PAN ID: "));
    USB.printHex(xbeeZB.operating64PAN[0]);
    USB.printHex(xbeeZB.operating64PAN[1]);
    USB.printHex(xbeeZB.operating64PAN[2]);
    USB.printHex(xbeeZB.operating64PAN[3]);
    USB.printHex(xbeeZB.operating64PAN[4]);
    USB.printHex(xbeeZB.operating64PAN[5]);
    USB.printHex(xbeeZB.operating64PAN[6]);
    USB.printHex(xbeeZB.operating64PAN[7]);
    USB.println();     
    
    xbeeZB.getAssociationIndication();
  }

  USB.println(F("\nJoined a network!"));

  // 3. get network parameters 
  xbeeZB.getOperating16PAN();
  xbeeZB.getOperating64PAN();
  xbeeZB.getChannel();

  USB.print(F("operating 16-b PAN ID: "));
  USB.printHex(xbeeZB.operating16PAN[0]);
  USB.printHex(xbeeZB.operating16PAN[1]);
  USB.println();

  USB.print(F("operating 64-b PAN ID: "));
  USB.printHex(xbeeZB.operating64PAN[0]);
  USB.printHex(xbeeZB.operating64PAN[1]);
  USB.printHex(xbeeZB.operating64PAN[2]);
  USB.printHex(xbeeZB.operating64PAN[3]);
  USB.printHex(xbeeZB.operating64PAN[4]);
  USB.printHex(xbeeZB.operating64PAN[5]);
  USB.printHex(xbeeZB.operating64PAN[6]);
  USB.printHex(xbeeZB.operating64PAN[7]);
  USB.println();

  USB.print(F("channel: "));
  USB.printHex(xbeeZB.channel);
  USB.println();

}


void loop()
{
  // receive XBee packet (wait for 10 seconds)
  error = xbeeZB.receivePacketTimeout(10000);

  // check answer  
  if( error == 0 ) 
  {
    dest[0] = xbeeZB._srcMAC[0]; 
    dest[1] = xbeeZB._srcMAC[1]; 
    dest[2] = xbeeZB._srcMAC[2]; 
    dest[3] = xbeeZB._srcMAC[3]; 
    dest[4] = xbeeZB._srcMAC[4]; 
    dest[5] = xbeeZB._srcMAC[5]; 
    dest[6] = xbeeZB._srcMAC[6]; 
    dest[7] = xbeeZB._srcMAC[7]; 

    //received from GW
    if(dest[7] == macGW_lastHEX) {
      
        USB.println(F("Received from GW, passing through to R2"));

        xbeeZB.send(RX_ADDRESS, xbeeZB._payload, xbeeZB._length);        

    } 
    else if(dest[7] == macED1_lastHEX)
    {

      USB.println("Interrupt -- source: ED1, sending to GW");
      USB.println("acc = 1.0");

    
      acc = 1.0;
      Events.ON();
      
      temp = Events.getTemperature();
      humid = Events.getHumidity();
      
      frame.createFrame(ASCII);
      frame.addSensor(SENSOR_ACC, acc);
      frame.addSensor(SENSOR_EVENTS_TC, temp);
      frame.addSensor(SENSOR_EVENTS_HUM, humid);
      
      xbeeZB.send(GW_ADDRESS, frame.buffer, frame.length);

      USB.print("temp: ");
      USB.println(temp);
      USB.print("humid: ");
      USB.println(humid);
      
    } else {
      
      USB.print(F("Error"));
      
    }  
  } else
  {

    USB.println("Passing through to GW, no interrupt");
    USB.println("acc = 0.0");
    
    acc = 0.0;
    Events.ON();
    
    temp = Events.getTemperature();
    humid = Events.getHumidity();
    
    frame.createFrame(ASCII);
    frame.addSensor(SENSOR_ACC, acc);
    frame.addSensor(SENSOR_EVENTS_TC, temp);
    frame.addSensor(SENSOR_EVENTS_HUM, humid);
    
    xbeeZB.send(GW_ADDRESS, frame.buffer, frame.length);
    xbeeZB.send(RX_ADDRESS, frame.buffer, frame.length);

    USB.print("temp: ");
    USB.println(temp);
    USB.print("humid: ");
    USB.println(humid);    
  }
}



