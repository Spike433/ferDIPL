/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package hr.fer.tel.rassus.pdq.homework;

import com.perfdynamics.pdq.Job;
import com.perfdynamics.pdq.Methods;
import com.perfdynamics.pdq.Node;
import com.perfdynamics.pdq.PDQ;
import com.perfdynamics.pdq.QDiscipline;

public class Main {

    public static void main(String[] args) {
        PDQ pdq = new PDQ();

        final float v1 = 1.0f;
        final float v2 = 1.2195f;
        final float v3 = 0.3762f;
        final float v4 = 0.4411f;
        final float v5 = 0.6098f;
        final float v6 = 0.3659f;
        final float v7 = 0.8536f;

        final float S1 = 0.003f;
        final float S2 = 0.001f;
        final float S3 = 0.01f;
        final float S4 = 0.04f;
        final float S5 = 0.1f;
        final float S6 = 0.13f;
        final float S7 = 0.15f;

        final int lambda_max = 20; // 20 represents 2.0 as maximum value
        float lambda;

        for (int i = 1; i < lambda_max + 1; i++) {
            lambda = (float) i/10;
            pdq.Init("Task");
            pdq.CreateOpen("Packages", lambda);

            pdq.CreateNode("N1", Node.CEN, QDiscipline.FCFS);
            pdq.CreateNode("N2", Node.CEN, QDiscipline.FCFS);
            pdq.CreateNode("N3", Node.CEN, QDiscipline.FCFS);
            pdq.CreateNode("N4", Node.CEN, QDiscipline.FCFS);
            pdq.CreateNode("N5", Node.CEN, QDiscipline.FCFS);
            pdq.CreateNode("N6", Node.CEN, QDiscipline.FCFS);
            pdq.CreateNode("N7", Node.CEN, QDiscipline.FCFS);

            pdq.SetVisits("N1", "Packages", v1, S1);
            pdq.SetVisits("N2", "Packages", v2, S2);
            pdq.SetVisits("N3", "Packages", v3, S3);
            pdq.SetVisits("N4", "Packages", v4, S4);
            pdq.SetVisits("N5", "Packages", v5, S5);
            pdq.SetVisits("N6", "Packages", v6, S6);
            pdq.SetVisits("N7", "Packages", v7, S7);

            pdq.Solve(Methods.CANON);

            System.out.println("lambda: " + lambda);
            System.out.println("T1: " + pdq.GetResidenceTime("N1", "Packages", Job.TRANS) + "\t");
            System.out.println("T2: " + pdq.GetResidenceTime("N2", "Packages", Job.TRANS) + "\t");
            System.out.println("T3: " + pdq.GetResidenceTime("N3", "Packages", Job.TRANS) + "\t");
            System.out.println("T4: " + pdq.GetResidenceTime("N4", "Packages", Job.TRANS) + "\t");
            System.out.println("T5: " + pdq.GetResidenceTime("N5", "Packages", Job.TRANS) + "\t");
            System.out.println("T6: " + pdq.GetResidenceTime("N6", "Packages", Job.TRANS) + "\t");
            System.out.println("T7: " + pdq.GetResidenceTime("N7", "Packages", Job.TRANS) + "\t");
            System.out.println("T: " + pdq.GetResponse(Job.TRANS, "Packages"));
            System.out.println();
        }
    }
}