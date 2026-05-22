
from tical_code.guardian.models import InteractionSignal
from tical_code.guardian.state_classifier import StateClassifier
def test_focus():
    s=InteractionSignal(input_interval_variance=1)
    assert StateClassifier().classify(s).state in ["FOCUS","REST"]
