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

@dataclass(frozen=True)
class PrepareCallbacksConfig:
    root_dir: Path
    tensorboard_root_log_dir: Path
    checkpoint_model_filepath: Path

@dataclass(frozen=True)
class TrainingConfig:
    root_dir: Path
    trained_model_path: Path
    updated_base_model_path: Path
    training_data: Path
    params_epochs: int
    params_batch_size: int
    params_is_augmentation: bool
    params_image_size: list

@dataclass(frozen=True)
class EvaluationConfig:
    path_of_model: Path
    training_data: Path
    params_image_size: list
    params_batch_size: int