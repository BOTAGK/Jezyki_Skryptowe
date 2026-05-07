from typing import List
from station_manager import Measurement

class AnomalyDetector:
    def __init__(self, spike_threshold: float = 50.0, alarm_threshold: float = 200.0):
        
        self.spike_threshold = spike_threshold
        self.alarm_threshold = alarm_threshold

    def analyze(self, measurements: List[Measurement]) -> List[str]:
        """Analizuje listę pomiarów i zwraca listę tekstów opisujących wykryte anomalie."""
        anomalies = []
        if not measurements:
            return anomalies

        sorted_m = sorted(measurements, key=lambda x: x.timestamp)
        
        zero_count = 0
        
        for i, m in enumerate(sorted_m):
            # Negative value rule
            if m.value < 0:
                anomalies.append(f"[{m.timestamp}] BŁĄD: Wartość ujemna ({m.value} {m.unit})")
            
            # Frozen sensor rule: 4 consecutive zero readings
            if m.value == 0.0:
                zero_count += 1
                if zero_count == 4:
                    anomalies.append(f"[{m.timestamp}] AWARIA: Wykryto 4 zerowe pomiary z rzędu!")
            else:
                zero_count = 0 
            
            # Surpassing alarm threshold rule 
            if m.value > self.alarm_threshold:
                anomalies.append(f"[{m.timestamp}] ALARM: Kosmiczna wartość pomiaru ({m.value} {m.unit})")
            
            # Spike detection rule: sudden jump compared to previous measurement
            if i > 0:
                prev_m = sorted_m[i-1]
                delta = abs(m.value - prev_m.value)
                if delta > self.spike_threshold:
                    anomalies.append(f"[{m.timestamp}] SKOK: Nienaturalny skok o {delta:.2f} {m.unit} (z {prev_m.value} na {m.value})")

        return anomalies