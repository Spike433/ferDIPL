package hr.fer.tel.rassus.sensorAndProducer;

import hr.fer.tel.rassus.readingSensorModel.ReadingModel;

import java.util.Comparator;

public class CustomScalarComparator implements Comparator<ReadingModel> {

    @Override
    public int compare(ReadingModel o1, ReadingModel o2) {
        if(o1.getVectorTime() == o2.getVectorTime())
        {
            return o1.getScalarTime() < o2.getScalarTime() ? 1 : -1;
        }

        return o1.getVectorTime() < o2.getVectorTime() ? 1 : -1;
    }
}
