import React, { useState } from "react";
import DataComponent from "../../components/DataComponent/DataComponent";
import styles from "./GraphPage.module.css";
import { Button } from "@mui/material";

function GraphPage() {
  const [page, setPage] = useState(0);

  const pages = [
    { name: "Temperature", url: "G23Temp" },
    { name: "Ph", url: "G23ph" },
    { name: "Solids", url: "G23Solids" },
  ];
  console.log("rerendero sam ", page, pages[page]);
  return (
    <div>
      <div className={styles.buttonsDiv}>
        <Button variant="outlined" onClick={() => setPage(0)}>
          Temperature
        </Button>
        <Button variant="outlined" onClick={() => setPage(1)}>
          Ph
        </Button>
        <Button variant="outlined" onClick={() => setPage(2)}>
          Solids
        </Button>
      </div>
      <DataComponent data={pages[page]} />
    </div>
  );
}

export default GraphPage;
