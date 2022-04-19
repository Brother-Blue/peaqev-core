
class ChargeContollerBase:
    @staticmethod
    def below_start_threshold(
            predicted_energy: float,
            current_peak: float,
            threshold_start: float
    ) -> bool:
        return (predicted_energy * 1000) < ((current_peak * 1000) * (threshold_start / 100))

    @staticmethod
    def above_stop_threshold(
            predicted_energy: float,
            current_peak: float,
            threshold_stop: float
    ) -> bool:
        return (predicted_energy * 1000) > ((current_peak * 1000) * (threshold_stop / 100))