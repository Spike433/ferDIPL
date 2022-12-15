package hr.fer.tel.rassus.sensorAndProducer;

import hr.fer.tel.rassus.readingSensorModel.ReadingModel;
import hr.fer.tel.rassus.readingSensorModel.SensorModel;
import hr.fer.tel.rassus.stupidudpTemplate.network.EmulatedSystemClock;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class SensConstants {
    public static Map<SensorModel, List<SensorModel>> sensVect = new HashMap<>();
    public static final String RegosterTopic = "Register";
    public static final String CommandTopic = "Command";
    public  static Boolean StartProducer = false;
    public static Boolean StopProducer = false;

    public static SensorModel sensorModel;
    public static Long StartingTime = 0L;
    public static String Port = "";
    public static final EmulatedSystemClock emulatedSystemClock = new EmulatedSystemClock();
    public static List<ReadingModel> gotReadingModels = new ArrayList<>();
    public static List<ReadingModel> mySensorReadingModels = new ArrayList<>();


}


