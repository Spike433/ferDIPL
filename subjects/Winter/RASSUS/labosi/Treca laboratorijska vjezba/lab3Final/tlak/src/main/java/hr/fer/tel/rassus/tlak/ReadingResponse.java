package hr.fer.tel.rassus.tlak;

public class ReadingResponse {
    private final String name = "Humidity";
    private final String unit = "%";
    private int value;

    public ReadingResponse() {
    }

    public ReadingResponse(int value) {
        this.value = value;
    }

    public ReadingResponse(Reading reading) {
        this.value = reading.getValue();
    }

    public String getName() {
        return name;
    }

    public String getUnit() {
        return unit;
    }

    public int getValue() {
        return value;
    }

    public void setValue(int value) {
        this.value = value;
    }
}
