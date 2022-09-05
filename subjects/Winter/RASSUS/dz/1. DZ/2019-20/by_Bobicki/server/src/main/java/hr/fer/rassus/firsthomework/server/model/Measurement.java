package hr.fer.rassus.firsthomework.server.model;

public class Measurement {
    private String username;
    private String parameter;
    private float averageValue;

    public Measurement() {
    }

    public Measurement(String username, String parameter, float averageValue) {
        this.username = username;
        this.parameter = parameter;
        this.averageValue = averageValue;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getParameter() {
        return parameter;
    }

    public void setParameter(String parameter) {
        this.parameter = parameter;
    }

    public float getAverageValue() {
        return averageValue;
    }

    public void setAverageValue(float averageValue) {
        this.averageValue = averageValue;
    }

    @Override
    public String toString() {
        return "username='" + username + '\'' +
                ", parameter='" + parameter + '\'' +
                ", averageValue=" + averageValue;
    }
}