import typer
from datetime import datetime
from pathlib import Path
from enum import Enum
from dataclasses import dataclass
import random
import statistics

from station_manager import StationManager
from anomaly_detector import AnomalyDetector

class MetricType(str, Enum):
    PM10 = "PM10"
    PM25 = "PM2.5"
    HG = "Hg(TGM)"
    NO2 = "NO2"
    

class FreqType(str, Enum):
    H1 = "1g"
    H24 = "24g"

@dataclass
class AppState:
    manager: StationManager
    metric: MetricType
    start: datetime
    end: datetime


app = typer.Typer(help="Analizator danych GIOŚ (wersja Typer - Clean Code)")

@app.callback()
def main_callback(
    ctx: typer.Context,
    
    metric: MetricType = typer.Option(..., help="Mierzona wielkość"),
    freq: FreqType = typer.Option(..., help="Częstotliwość"),
    start: datetime = typer.Option(..., formats=["%Y-%m-%d"], help="Początek (RRRR-MM-DD)"),
    end: datetime = typer.Option(..., formats=["%Y-%m-%d"], help="Koniec (RRRR-MM-DD)"),
    data_dir: Path = typer.Option(Path(__file__).with_name("data"), help="Główny katalog z danymi")
):
    """Global parameters for the entire application."""
    
    metadata_path = data_dir / "station" / "stacje.csv"
    manager = StationManager(metadata_path)
    
    rok = start.year
    measurement_file = data_dir / "measurements" / f"{rok}_{metric.value}_{freq.value}.csv"
    
    if measurement_file.exists():
        manager.parse_measurement_file(measurement_file)
    else:
        typer.secho(f"Ostrzeżenie: Nie znaleziono pliku {measurement_file}!", fg=typer.colors.YELLOW)
    
    ctx.obj = AppState(
        manager=manager,
        metric=metric,
        start=start,
        end=end
    )

@app.command("random")
def random_station(ctx: typer.Context):
    """Writes info about a random station that has measurements in the given time range."""
    
    state: AppState = ctx.obj
    
    valid_station_codes = set()
    for code, pomiary in state.manager.measurements_data.items():
        for p in pomiary:
            if state.start <= p.timestamp <= state.end:
                valid_station_codes.add(code)
                break 
                
    if not valid_station_codes:
        typer.secho("Brak pomiarów dla tych parametrów w danym czasie.", fg=typer.colors.RED)
        raise typer.Exit()
        
    chosen_code = random.choice(list(valid_station_codes))
    stacja = state.manager.stations_data.get(chosen_code)
    
    if stacja:
        typer.secho("\n--- WYLOSOWANA STACJA ---", fg=typer.colors.GREEN, bold=True)
        print(f"Nazwa: {stacja.name}")
        print(f"Adres: {stacja.city}, {stacja.address}")
        print(f"Kod:   {stacja.code}\n")


@app.command("worst")
def worst_station(ctx: typer.Context):
    state: AppState = ctx.obj
    
    worst_code = None
    worst_avg = 0.0

    for code, measurements in state.manager.measurements_data.items():
        values = []
        for m in measurements:
            if state.start <= m.timestamp <= state.end:
                values.append(m.value)

        if values:
            avg = statistics.mean(values)
            if avg > worst_avg:
                worst_avg = avg
                worst_code = code
                
    if worst_code is None:
        typer.secho("Brak pomiarów dla tych parametrów w danym czasie.", fg=typer.colors.RED)
        raise typer.Exit()
        
    station = state.manager.stations_data.get(worst_code)
    
    if station:
        typer.secho("\n--- NAJGORSZA STACJA ---", fg=typer.colors.RED, bold=True)
        print(f"Nazwa: {station.name}")
        print(f"Adres: {station.city}, {station.address}")
        print(f"Kod:   {station.code}")
        print(f"Średnia wartość: {worst_avg:.4f}\n")

@app.command("stats")
def station_stats(
    ctx: typer.Context, 
    station: str = typer.Option(..., help="Kod stacji (np. DsOsieczow21)")
):
    """Counts and calculates mean and standard deviation for a given station and time range."""
    
    state: AppState = ctx.obj
    
    if station not in state.manager.measurements_data:
        typer.secho(f"Brak danych pomiarowych dla stacji {station}.", fg=typer.colors.RED)
        raise typer.Exit()
        
    wartosci = [
        p.value for p in state.manager.measurements_data[station]
        if state.start <= p.timestamp <= state.end
    ]
    
    if not wartosci:
        typer.secho(f"Stacja {station} nie ma pomiarów w zadanym okresie.", fg=typer.colors.RED)
    elif len(wartosci) < 2:
        typer.secho("Zbyt mało danych do obliczenia odchylenia standardowego (wymagane min. 2).", fg=typer.colors.YELLOW)
    else:
        srednia = statistics.mean(wartosci)
        odchylenie = statistics.stdev(wartosci)
        
        typer.secho(f"\n--- STATYSTYKI: {station} ({state.metric.value}) ---", fg=typer.colors.CYAN, bold=True)
        print(f"Ilość pomiarów:         {len(wartosci)}")
        print(f"Średnia:                {srednia:.4f}")
        print(f"Odchylenie standardowe: {odchylenie:.4f}\n")

@app.command("anomalies")
def find_anomalies(
    ctx: typer.Context, 
    station: str = typer.Option(..., help="Kod stacji (np. DsOsieczow21)")
):
    """Scans measurements for a given station and time range, looking for anomalies based on predefined rules."""
    
    state: AppState = ctx.obj
    
    if station not in state.manager.measurements_data:
        typer.secho(f"Brak danych pomiarowych dla stacji {station}.", fg=typer.colors.RED)
        raise typer.Exit()
        
    pomiary = [
        p for p in state.manager.measurements_data[station]
        if state.start <= p.timestamp <= state.end
    ]
    
    if not pomiary:
        typer.secho(f"Stacja {station} nie ma pomiarów w zadanym okresie.", fg=typer.colors.RED)
        raise typer.Exit()
        
    typer.secho(f"\nSkanowanie {len(pomiary)} pomiarów stacji {station} ({state.metric.value})...", fg=typer.colors.CYAN)

    if state.metric.value == "Hg(TGM)":
        detector = AnomalyDetector(spike_threshold=1.0, alarm_threshold=5.0)
    else:
        detector = AnomalyDetector(spike_threshold=50.0, alarm_threshold=200.0)
        
    znalezione_anomalie = detector.analyze(pomiary)

    if znalezione_anomalie:
        typer.secho(f"Wykryto {len(znalezione_anomalie)} anomalii!", fg=typer.colors.RED, bold=True)
        for anomalia in znalezione_anomalie[:15]:
            print(f" - {anomalia}")
            
        if len(znalezione_anomalie) > 15:
            print(f" ...oraz {len(znalezione_anomalie) - 15} kolejnych błędów ukryto.")
    else:
        typer.secho("Nie wykryto żadnych anomalii! Czujnik działa prawidłowo.", fg=typer.colors.GREEN, bold=True)        

if __name__ == "__main__":
    app()