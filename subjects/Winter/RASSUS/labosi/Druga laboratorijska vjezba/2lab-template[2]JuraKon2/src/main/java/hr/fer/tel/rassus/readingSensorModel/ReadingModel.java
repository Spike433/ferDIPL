package hr.fer.tel.rassus.readingSensorModel;

import java.io.Serializable;
import com.opencsv.bean.CsvBindByName;
import lombok.Data;
@Data
public class ReadingModel implements Serializable {

    @CsvBindByName
    private int NO2;
    private long scalarTime;
    private int vectorTime;
    private int sensorId;


    public ReadingModel()
    {

    }

    @Override
    public String toString() {
        return "Reading from CSV -->" +
            "\n sensorId -->" + sensorId +
            "\n vectorTime -->" + vectorTime +
            "\n scalarTime -->" + scalarTime +
            "\n NO2 -->" + NO2;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        ReadingModel readingModel = (ReadingModel) o;
        return NO2 == readingModel.NO2 &&
               scalarTime == readingModel.scalarTime &&
               vectorTime == readingModel.vectorTime &&
               sensorId == readingModel.sensorId;
    }

    @Override
    public int hashCode() {
        return super.hashCode();
    }
}
