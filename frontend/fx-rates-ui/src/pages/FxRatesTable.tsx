import { useEffect, useState } from "react";

interface ApiRate {
  fecha: string;
  tipo_tasa: string;
  from_moneda: string;
  to_moneda: string;
  factor: number;
}

interface RatePair {
  usdTo: number | null; // 1 USD = Moneda
  toUsd: number | null; // 1 Moneda = USD
}

interface RatesMap {
  [currency: string]: RatePair;
}



const FxRatesTable = () => {
  const [rates, setRates] = useState<RatesMap>({});
  const [date, setDate] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    /*fetch("https://api.frankfurter.app/latest?base=USD")*/
    fetch("https://tasasdecambiousd-backend.onrender.com/api/tasas/prueba?fecha=2026-02-05")
      .then((res) => {
        if (!res.ok) {
          throw new Error("Error al consumir la API de tasas");
        }
        return res.json();
      })
      .then((data: ApiRate[]) => {
        const map: RatesMap = {};

        data.forEach((item) => {
          const currency =
            item.from_moneda === "USD"
              ? item.to_moneda
              : item.from_moneda;

          if (!map[currency]) {
            map[currency] = { usdTo: null, toUsd: null };
          }
          
          if (item.from_moneda === "USD") {
            map[currency].usdTo = item.factor;
          }

          if (item.to_moneda === "USD") {
            map[currency].toUsd = item.factor;
          }        

        });

        setRates(map);
        setDate(data[0]?.fecha ?? "");
        setLoading(false);
      })        

      .catch((err: Error) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Cargando tasas de cambio...</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;

  const renderRow = (name: string, code: string) => (
    <tr>
      <td>{name}</td>
      <td>{code}</td>
      <td>{rates[code]?.usdTo?.toFixed(6) ?? "-"}</td>
      <td>{rates[code]?.toUsd?.toFixed(6) ?? "-"}</td>
    </tr>
  );

  return (
    <div style={{ padding: "20px" }}>
      <h2>Tasa media – Conversión a USD</h2>
      <p>
        <strong>Fuente:</strong> Banco de la República <br />
        <strong>Fecha:</strong> {date}
      </p>

      <table
        border={1}
        cellPadding={8}
        style={{ borderCollapse: "collapse", width: "100%" }}
      >
        <thead>
          <tr>
            <th>Moneda</th>
            <th>Código</th>
            <th>1 USD = Moneda</th>
            <th>1 Moneda = USD</th>
          </tr>
        </thead>
        <tbody>
          {renderRow("Yen Japonés", "JPY")}
          {renderRow("Peso Mexicano", "MXN")}
          {renderRow("Dólar Canadiense", "CAD")}
          {renderRow("Euro", "EUR")}
          {renderRow("Libra Esterlina", "GBP")}
          {renderRow("Dólar Singapur", "SGD")}
          {renderRow("Franco Suizo", "CHF")}
   
             
                            
        </tbody>
      </table>
    </div>
  );
};

export default FxRatesTable;
