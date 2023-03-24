
// Put your libraries here (#include ...)
#include <WaspXBeeZB.h>
#include <WaspFrame.h>

uint8_t msg;


uint8_t status;

int x_acc;
int y_acc;
int z_acc;


// Destination MAC address

char R1_ADDRESS[] = "0013A20040F8DBFC";

// Define the Waspmote ID

char WASPMOTE_ID[] = "node_01";

uint8_t  PANID[8] = {0x33, 0x44, 0x55, 0x66, 0x77, 0x88, 0x99,  0x11};



void setup()
{
  ACC.ON();
  USB.ON();
  frame.setID( WASPMOTE_ID );
  xbeeZB.ON();                                   
  
  delay(2000);
  
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

  USB.println(F("------------------------------"));

  xbeeZB.setSleepMode(1);
  
  ///////////////////////////////////////////////
  // Save values
  ///////////////////////////////////////////////
  
  xbeeZB.writeValues();
  USB.println();

  // wait for the module to set the parameters
  delay(900);

  
  //////////////////////////
  // 2. check XBee's network parameters
  //////////////////////////
  
  
  checkNetworkParams();
  

  delay(1500);
}


void loop()
{
  
  //----------Check Register-----------------------
  // should always answer 0x32, it is used to check
  // the proper functionality of the accelerometer

  //  ACC.ON();
  //  ACC.setMode(ACC_LOW_POWER_1);
  
  //  ACC.setMode(ACC_LOW_POWER_2);
  
  //  ACC.setMode(ACC_LOW_POWER_3);
  
  
  ACC.setMode(ACC_ON);
  
  status = ACC.check();
  
  
  x_acc = ACC.getX();

  y_acc = ACC.getY();

  z_acc = ACC.getZ();


  USB.println(F("\n------------------------------"));
  USB.println(F("\nAccelerometer mode: ACC_ON"));
  //  USB.println(F("\nAccelerometer mode: ACC_LOW_POWER_1"));
  //  USB.println(F("Accelerometer mode: ACC_LOW_POWER_2"));
  //  USB.println(F("Accelerometer mode: ACC_LOW_POWER_3"));
  USB.print(F("\n------------------------------\nCheck: 0x")); 
  USB.println(status, HEX);
  USB.println(F("\n \t0X\t0Y\t0Z")); 
  USB.print(F(" ACC\t")); 
  USB.print(x_acc, DEC);
  USB.print(F("\t")); 
  USB.print(y_acc, DEC);
  USB.print(F("\t")); 
  USB.println(z_acc, DEC);

  ///////////////////////////////////////////////
  // 2. Enable interruption: Inertial Wake Up
  ///////////////////////////////////////////////
  ACC.setIWU();

  ///////////////////////////////////////////////
  // 3. Set low-power consumption state
  ///////////////////////////////////////////////
  USB.println(F("\nWaspmote goes into sleep mode until the Accelerometer causes an interrupt"));
  PWR.sleep(ALL_OFF); 

  ///////////////////////////////////////////////
  // 4. Disable interruption: Inertial Wake Up
  //    This is done to avoid new interruptions
  ///////////////////////////////////////////////
  ACC.ON();
  ACC.unsetIWU(); 


  USB.ON();
  USB.println(F("\nWaspmote wakes up"));

  ///////////////////////////////////////////////
  // 5. Check the interruption source 
  ///////////////////////////////////////////////
   if( intFlag & ACC_INT )
  {
    // clear interruption flag
    intFlag &= ~(ACC_INT);
    
    // print info
    USB.ON();
    USB.println(F("\n++++++++++++++++++++++++++++"));
    USB.println(F("++ ACC interrupt detected ++"));
    USB.println(F("++++++++++++++++++++++++++++")); 
    USB.println(); 

    // blink LEDs
    for(int i=0; i<20; i++)
    {
      Utils.blinkLEDs(200);
    }    
  }

  ///////////////////////////////////////////////////////////////////////
  // 6. Clear interruption pin   
  ///////////////////////////////////////////////////////////////////////
  
  // This function is used to make sure the interruption pin is cleared
  // if a non-captured interruption has been produced
  
  PWR.clearInterruptionPin();

  delay(1000);

  // create new frame
  frame.createFrame(ASCII);  
  
  // add frame fields
  //frame.addSensor(SENSOR_BAT, PWR.getBatteryLevel());
  frame.addSensor(SENSOR_ACC, x_acc);
  frame.addSensor(SENSOR_ACC, y_acc);
  frame.addSensor(SENSOR_ACC, z_acc);

  xbeeZB.ON();
  
  msg = xbeeZB.send( R1_ADDRESS, frame.buffer, frame.length );   
  
  
  if( msg == 0 )
  {
    USB.println(F("send ok"));
    
    // blink green LED
    Utils.blinkGreenLED(100);
    
  }
  else 
  {
    USB.println(F("send error"));
    
    // blink red LED
    Utils.blinkRedLED(100);
  }

  // wait for 2 seconds
  delay(2000);
}

void checkNetworkParams()
{
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

  USB.println(F("\nJoined a network!eeee"));

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



