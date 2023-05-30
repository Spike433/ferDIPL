package hr.fer.zkist.ppks.readings;

import com.google.gson.Gson;

/**
 *
 * @author Krešimir Pripužić <kresimir.pripuzic@fer.hr>
 */
public class Reading {

    private static final Gson gson = new Gson();

    private final String sensorId;
    private final String quantity; //what is measured
    private final double value;
    private final String unit;

    public Reading(String sensorId, String quantity, double value, String unit) {
        this.sensorId = sensorId;
        this.quantity = quantity;
        this.value = value;
        this.unit = unit;
    }

    public String getSensorId() {
        return sensorId;
    }

    public String getQuantity() {
        return quantity;
    }

    public double getValue() {
        return value;
    }

    public String getUnit() {
        return unit;
    }

    @Override
    public String toString() {
        return "Reading{" + "sensorId=" + sensorId + ", quantity=" + quantity + ", value=" + value + ", unit=" + unit + '}';
    }

    public String toJson() {
        return gson.toJson(this);
    }

    public static Reading fromJson(String json) {
        return (Reading) gson.fromJson(json, Reading.class);
    }
}
