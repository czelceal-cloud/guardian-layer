
from tical_code.guardian.signal_collector import SignalCollector
from tical_code.guardian.state_classifier import StateClassifier
def guardian_patrol():
    sig=SignalCollector().collect()
    return StateClassifier().classify(sig)
