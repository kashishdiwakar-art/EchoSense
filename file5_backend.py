import io
import os
import pickle
import warnings
import numpy as np
from pathlib import Path

import librosa
import soundfile as sf

warnings.filterwarnings("ignore")


_MODELS   = {}
_SCALER   = None
_LE       = None
_READY    = False

SAMPLE_RATE   = 22050
CLIP_DURATION = 5.0
HOP_LENGTH    = 512
N_FFT         = 2048
N_MELS        = 128
N_MFCC        = 40


def load_echosense_model(model_dir: str = "echosense_model") -> bool:
    """
    Load all model components from disk into module-level globals.
    Returns True if successful, False otherwise.
    """
    global _MODELS, _SCALER, _LE, _READY

    model_path = Path(model_dir)
    required   = ["RandomForest.pkl", "SVM_RBF.pkl",
                   "GradientBoosting.pkl", "scaler.pkl", "label_encoder.pkl"]

    # Check all files exist
    missing = [f for f in required if not (model_path / f).exists()]
    if missing:
        print(f"[EchoSense Backend] Missing model files: {missing}")
        _READY = False
        return False

    try:
        _MODELS = {}
        for name in ["RandomForest", "SVM_RBF", "GradientBoosting"]:
            with open(model_path / f"{name}.pkl", "rb") as f:
                _MODELS[name] = pickle.load(f)

        with open(model_path / "scaler.pkl", "rb") as f:
            _SCALER = pickle.load(f)

        with open(model_path / "label_encoder.pkl", "rb") as f:
            _LE = pickle.load(f)

        _READY = True
        print(f"[EchoSense Backend] Model loaded. "
              f"{len(_LE.classes_)} classes, "
              f"{len(_MODELS)} sub-models.")
        return True

    except Exception as e:
        print(f"[EchoSense Backend] Load error: {e}")
        _READY = False
        return False


def is_model_ready() -> bool:
    """Check whether the model has been loaded successfully."""
    return _READY


def _load_audio(source):
    """
    Load audio from a file path (str/Path) or bytes buffer.
    Returns a numpy float32 array at SAMPLE_RATE, or None on failure.
    """
    try:
        if isinstance(source, (str, Path)):
            audio, _ = librosa.load(str(source), sr=SAMPLE_RATE,
                                    mono=True, duration=CLIP_DURATION)
        else:
            # bytes / BytesIO buffer
            if isinstance(source, bytes):
                source = io.BytesIO(source)
            audio, _ = librosa.load(source, sr=SAMPLE_RATE,
                                    mono=True, duration=CLIP_DURATION)
    except Exception as e:
        print(f"[Backend] load_audio error: {e}")
        return None

    target = int(SAMPLE_RATE * CLIP_DURATION)
    if len(audio) < target:
        audio = np.pad(audio, (0, target - len(audio)), mode="constant")
    return audio[:target].astype(np.float32)


def _spectral_subtract(audio: np.ndarray) -> np.ndarray:
    """
    Reduce stationary background noise via spectral subtraction.
    Estimates noise floor from first 10 STFT frames.
    """
    stft       = librosa.stft(audio, n_fft=N_FFT, hop_length=HOP_LENGTH)
    mag, phase = np.abs(stft), np.angle(stft)
    noise      = np.mean(mag[:, :10], axis=1, keepdims=True)
    mag_clean  = np.maximum(mag - noise, 0.0)
    stft_clean = mag_clean * np.exp(1j * phase)
    out        = librosa.istft(stft_clean, hop_length=HOP_LENGTH)
    target     = int(SAMPLE_RATE * CLIP_DURATION)
    if len(out) < target:
        out = np.pad(out, (0, target - len(out)))
    return out[:target].astype(np.float32)


def _remove_silence(audio: np.ndarray, top_db: int = 25) -> np.ndarray:
    """Trim leading/trailing silence, re-pad to fixed length."""
    trimmed, _ = librosa.effects.trim(audio, top_db=top_db)
    target     = int(SAMPLE_RATE * CLIP_DURATION)
    if len(trimmed) < target:
        trimmed = np.pad(trimmed, (0, target - len(trimmed)))
    return trimmed[:target].astype(np.float32)


def _has_signal(audio: np.ndarray, threshold: float = 0.001) -> bool:
    """Return True if RMS energy indicates a real signal (not silence)."""
    return float(np.sqrt(np.mean(audio ** 2))) > threshold


def preprocess_audio(source) -> np.ndarray | None:
    """
    Full preprocessing pipeline:
        load → spectral subtract → silence removal → validate
    Returns clean float32 array or None if rejected.
    """
    audio = _load_audio(source)
    if audio is None:
        return None

    audio = _spectral_subtract(audio)
    audio = _remove_silence(audio)

    if not _has_signal(audio):
        return None

    return audio


def _mfcc(audio: np.ndarray) -> np.ndarray:
    """40 MFCCs × {mean, std, max, min} = 160 features."""
    m = librosa.feature.mfcc(y=audio, sr=SAMPLE_RATE, n_mfcc=N_MFCC,
                               n_fft=N_FFT, hop_length=HOP_LENGTH)
    return np.concatenate([m.mean(1), m.std(1), m.max(1), m.min(1)])


def _chroma(audio: np.ndarray) -> np.ndarray:
    """12 chroma × {mean, std} = 24 features."""
    c = librosa.feature.chroma_stft(y=audio, sr=SAMPLE_RATE,
                                     n_fft=N_FFT, hop_length=HOP_LENGTH)
    return np.concatenate([c.mean(1), c.std(1)])


def _spectral(audio: np.ndarray) -> np.ndarray:
    """Spectral descriptors: centroid, bandwidth, rolloff, zcr, contrast."""
    cen = librosa.feature.spectral_centroid(y=audio,  sr=SAMPLE_RATE, hop_length=HOP_LENGTH)
    bw  = librosa.feature.spectral_bandwidth(y=audio, sr=SAMPLE_RATE, hop_length=HOP_LENGTH)
    ro  = librosa.feature.spectral_rolloff(y=audio,   sr=SAMPLE_RATE, hop_length=HOP_LENGTH)
    zc  = librosa.feature.zero_crossing_rate(audio, hop_length=HOP_LENGTH)
    ct  = librosa.feature.spectral_contrast(y=audio,  sr=SAMPLE_RATE, hop_length=HOP_LENGTH)
    return np.concatenate([
        [cen.mean(), cen.std()],
        [bw.mean(),  bw.std()],
        [ro.mean(),  ro.std()],
        [zc.mean(),  zc.std()],
        ct.mean(1), ct.std(1),
    ])


def _tonnetz(audio: np.ndarray) -> np.ndarray:
    """Tonal centroid (tonnetz) 6 × 2 = 12 features."""
    harm = librosa.effects.harmonic(audio)
    tn   = librosa.feature.tonnetz(y=harm, sr=SAMPLE_RATE)
    return np.concatenate([tn.mean(1), tn.std(1)])


def extract_features(audio: np.ndarray) -> np.ndarray:
    """
    Combine all descriptors into one feature vector (~218 dims).
    Returns float32 array.
    """
    return np.concatenate([
        _mfcc(audio),
        _chroma(audio),
        _spectral(audio),
        _tonnetz(audio),
    ]).astype(np.float32)


def _soft_vote(features_scaled: np.ndarray) -> np.ndarray:
    """
    Average predicted probabilities across all sub-models.
    Returns 1-D probability array over all classes.
    """
    proba = None
    for model in _MODELS.values():
        p     = model.predict_proba(features_scaled)
        proba = p if proba is None else proba + p
    return (proba / len(_MODELS))[0]


def run_prediction(source, confidence_threshold: float = 0.40) -> dict:
    """
    End-to-end prediction from raw audio source.

    Parameters
    ----------
    source : str | Path | bytes | BytesIO
        Audio file path or raw bytes.
    confidence_threshold : float
        Below this, result is marked as 'Uncertain'.

    Returns
    -------
    dict with keys:
        prediction, species, category, confidence,
        top3, mel_spec, action
        OR
        error (str) on failure
    """
    if not _READY:
        return {"error": "Model is not loaded. Call load_echosense_model() first."}

    audio = preprocess_audio(source)
    if audio is None:
        return {"error": "Audio rejected — file may be silent, too short, or corrupt."}

    try:
        feats = extract_features(audio)
    except Exception as e:
        return {"error": f"Feature extraction failed: {e}"}

    if np.any(np.isnan(feats)) or np.any(np.isinf(feats)):
        return {"error": "Invalid feature values — try a different audio file."}

    feats_scaled = _SCALER.transform([feats])

    avg_proba = _soft_vote(feats_scaled)

    best_idx  = int(np.argmax(avg_proba))
    best_conf = float(avg_proba[best_idx])
    label     = _LE.classes_[best_idx]

    parts    = label.split("::")
    category = parts[0]          if len(parts) == 2 else "unknown"
    species  = parts[1]          if len(parts) == 2 else label

    top3_idx = np.argsort(avg_proba)[-3:][::-1]
    top3 = []
    for idx in top3_idx:
        lbl = _LE.classes_[idx]
        sp  = lbl.split("::")[-1] if "::" in lbl else lbl
        top3.append({
            "species":    sp,
            "confidence": round(float(avg_proba[idx]), 4),
        })

    mel    = librosa.feature.melspectrogram(
        y=audio, sr=SAMPLE_RATE,
        n_mels=N_MELS, n_fft=N_FFT, hop_length=HOP_LENGTH
    )
    mel_db = librosa.power_to_db(mel, ref=np.max)

    if best_conf < confidence_threshold:
        return {
            "prediction": "uncertain",
            "species":    "Unknown / Uncertain",
            "category":   "unknown",
            "confidence": round(best_conf, 4),
            "top3":       top3,
            "mel_spec":   mel_db,
            "action":     "Low confidence — saved for review",
        }

    return {
        "prediction": label,
        "species":    species,
        "category":   category,
        "confidence": round(best_conf, 4),
        "top3":       top3,
        "mel_spec":   mel_db,
        "action":     "Logged to dashboard",
    }


def get_waveform_data(source, max_points: int = 1000) -> tuple:
    """
    Load audio and return (time_array, amplitude_array) for plotting.
    Downsamples to max_points for performance.
    """
    audio = _load_audio(source)
    if audio is None:
        return np.array([]), np.array([])

    # Downsample for plotting
    if len(audio) > max_points:
        step  = len(audio) // max_points
        audio = audio[::step]

    duration = len(audio) / SAMPLE_RATE
    times    = np.linspace(0, duration, len(audio))
    return times, audio

def batch_predict(file_paths: list,
                  confidence_threshold: float = 0.40) -> list:
    """
    Run predictions on a list of audio file paths.
    Returns a list of result dicts (same format as run_prediction).
    """
    results = []
    for path in file_paths:
        result = run_prediction(path, confidence_threshold)
        result["file"] = str(path)
        results.append(result)
        print(f"  [{result.get('species','?')}] "
              f"{result.get('confidence',0)*100:.1f}% — {path}")
    return results


if __name__ == "__main__":
    import sys

    # Load model
    ok = load_echosense_model("echosense_model")
    if not ok:
        print("❌ Model not found. Run file2_model_training.py first.")
        sys.exit(1)

    print(f"✅ Model loaded. Ready: {is_model_ready()}\n")

    # Test with a file if provided
    if len(sys.argv) > 1:
        test_path = sys.argv[1]
        print(f"🔍 Predicting: {test_path}")
        result = run_prediction(test_path)

        if "error" in result:
            print(f"❌ Error: {result['error']}")
        else:
            print(f"\n  🐾 Species:    {result['species']}")
            print(f"  📂 Category:   {result['category']}")
            print(f"  📊 Confidence: {result['confidence']*100:.1f}%")
            print(f"  🏆 Top 3:")
            for t in result["top3"]:
                print(f"     • {t['species']}: {t['confidence']*100:.1f}%")
            print(f"  ⚡ Action:     {result['action']}")
    else:
        print("Usage: python file5_backend.py path/to/audio.wav")
        print("       (No test file provided — backend module is ready to import)\n")