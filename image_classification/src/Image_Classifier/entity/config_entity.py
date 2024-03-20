from dataclasses import dataclass
from pathlib import Path



@dataclass(frozen=True)
class DataIngestionConfig:
    saved_images: Path
    train_dir: Path  # Ensure the attribute name matches
    test_dir: Path
    test_ratio:int


@dataclass
class PrepareBaseModelConfig:
    root_dir_pre_model: Path
    updated_model: Path
    params_image_size: list
    params_include_top: bool
    params_weights: str
    params_neural: int
    params_loss: str
    params_optimizer: str
    params_learning_rate: float
    model_name:str
    freeze_all: bool
    freeze_till: int
