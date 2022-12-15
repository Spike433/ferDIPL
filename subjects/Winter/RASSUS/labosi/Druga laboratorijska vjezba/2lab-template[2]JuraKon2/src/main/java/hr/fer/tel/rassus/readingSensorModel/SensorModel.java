package hr.fer.tel.rassus.readingSensorModel;

import java.util.ArrayList;
import java.util.List;
import com.opencsv.bean.CsvBindByName;
import lombok.Data;

@Data
public class SensorModel {
    @CsvBindByName
    private int id;
    @CsvBindByName
    private String port;
    @CsvBindByName
    private int vectorValue;
    @CsvBindByName
    private String address;

    private List<SensorModel> neighbourArrayList;

    public SensorModel(int id, String address, String port) {
        this.id = id;
        this.address = address;
        this.neighbourArrayList = new ArrayList<>();
        this.port = port;
    }

    public SensorModel(){

    }
    public void addNeighbour(SensorModel sensorModel)
    {
        this.neighbourArrayList.add(sensorModel);

    }
    public List<SensorModel> getNeighbours()
    {
        return neighbourArrayList;
    }
    public String generateJsonData() {
        return "{\"id\": " + "\""
                + id + "\"" +
                ", \"address\" : "
                + "\"" +  address + "\"" +
                ", \"port\" : "
                + "\"" + port + "\"" +
                "}";
    }

    @Override
    public String toString() {
        return "Sensor{" +
                " id -->" + id +
                " adress  -->" + address +
                " port  -->" + port +
                " vector value -->" + vectorValue;
    }

    @Override
    public boolean equals(Object obj) {
        if (getClass() != obj.getClass() || obj == null) return false;
        if (this == obj) return true;
        SensorModel sensor = (SensorModel) obj;
        return id == sensor.id;
    }

    @Override
    public int hashCode() {
        return super.hashCode();
    }
}
