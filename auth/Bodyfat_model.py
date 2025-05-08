# auth/bodyfat_model.py

import io, os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import DepthwiseConv2D as _DepthwiseConv2D
from PIL import Image, ImageOps

# ────── 1) DepthwiseConv2D 그룹 인자 무시하는 서브클래스 ──────
class DepthwiseConv2D(_DepthwiseConv2D):
    def __init__(self, *args, groups=None, **kwargs):
        # groups 인자는 무시하고 부모 init 호출
        super().__init__(*args, **kwargs)

# ────── 2) 경로 설정 ──────
MODEL_PATH = os.getenv("BODYFAT_MODEL_PATH", "keras_Model.h5")
LABEL_PATH = os.getenv("BODYFAT_LABEL_PATH", "labels.txt")

# ────── 3) 모델·라벨 로드 ──────
# custom_objects 에 커스텀 레이어 지정
_model = load_model(MODEL_PATH, compile=False, custom_objects={"DepthwiseConv2D": DepthwiseConv2D})
with open(LABEL_PATH, "r") as f:
    _class_names = [line.strip() for line in f]

# ────── 4) 예측 함수 ──────
def predict_bodyfat(image_bytes: bytes):
    # 이미지 바이트 → PIL 이미지
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = ImageOps.fit(img, (224, 224), Image.Resampling.LANCZOS)

    # 배열 변환·정규화
    arr = np.asarray(img, dtype=np.float32)
    norm = (arr / 127.5) - 1
    batch = np.expand_dims(norm, axis=0)  # (1,224,224,3)

    # 예측
    preds = _model.predict(batch)
    idx = int(np.argmax(preds[0]))
    return _class_names[idx], float(preds[0][idx])\







