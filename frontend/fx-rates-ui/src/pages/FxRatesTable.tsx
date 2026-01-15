import { useEffect, useState } from "react";

interface Rates {
  [currency: string]: number;
}

interface FxApiResponse {
  base: string;
  date: string;
  rates: Rates;
}

const FxRatesTable = () => {
  const [rates, setRates] = useState<Rates>({});
  const [date, setDate] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("https://api.frankfurter.app/latest?base=USD")
      .then((res) => {
        if (!res.ok) {
          throw new Error("Error al consumir la API de tasas");
        }
        return res.json();
      })
      .then((data: FxApiResponse) => {
        setRates(data.rates);
        setDate(data.date);
        setLoading(false);
      })
      .catch((err: Error) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Cargando tasas de cambio...</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;

  return (
    <div style={{ padding: "20px" }}>
      <h2>Tasa media – Conversión a USD</h2>
      <p>
        <strong>Fuente:</strong> Frankfurter (ECB) <br />
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
          <tr>
            <td>Yen Japonés</td>
            <td>JPY</td>
            <td>{rates.JPY?.toFixed(6)}</td>
            <td>{rates.JPY ? (1 / rates.JPY).toFixed(6) : "-"}</td>
          </tr>
          <tr>
            <td>Peso Mexicano</td>
            <td>MXN</td>
            <td>{rates.MXN?.toFixed(6)}</td>
            <td>{rates.MXN ? (1 / rates.MXN).toFixed(6) : "-"}</td>
          </tr>
          <tr>
            <td>Dólar Canada</td>
            <td>CAD</td>
            <td>{rates.CAD?.toFixed(6)}</td>
            <td>{rates.CAD ? (1 / rates.CAD).toFixed(6) : "-"}</td>
          </tr>          
          <tr>
            <td>Euro</td>
            <td>EUR</td>
            <td>{rates.EUR?.toFixed(6)}</td>
            <td>{rates.EUR ? (1 / rates.EUR).toFixed(6) : "-"}</td>
          </tr>            
          <tr>
            <td>Libra Esterlina</td>
            <td>GBP</td>
            <td>{rates.GBP?.toFixed(6)}</td>
            <td>{rates.GBP ? (1 / rates.GBP).toFixed(6) : "-"}</td>
          </tr>        
          <tr>
            <td>Dólar Singapur</td>
            <td>SGD</td>
            <td>{rates.SGD?.toFixed(6)}</td>
            <td>{rates.SGD ? (1 / rates.SGD).toFixed(6) : "-"}</td>
          </tr>      
          <tr>
            <td>Franco Suizo</td>
            <td>CHF</td>
            <td>{rates.CHF?.toFixed(6)}</td>
            <td>{rates.CHF ? (1 / rates.CHF).toFixed(6) : "-"}</td>
          </tr>                        
        </tbody>
      </table>
    </div>
  );
};

export default FxRatesTable;
