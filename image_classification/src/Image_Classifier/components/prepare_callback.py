
import os
import tensorflow as tf
import time

class PrepareCallback:
    def __init__(self, config):
        self.config = config

    @property
    def _create_tb_callbacks(self):
        timestamp = time.strftime("%Y-%m-%d-%H-%M")
        tb_running_log_dir = os.path.join(
            self.config.tensorboard_root_log_dir,
            f"tb_logs_at_{timestamp}",
        )
        return tf.keras.callbacks.TensorBoard(log_dir=tb_running_log_dir)

    @property
    def _create_early_stopping_callback(self):
        return tf.keras.callbacks.EarlyStopping(
            monitor="accuracy",  # You can change "accuracy" to the quantity you want to monitor
            min_delta=0.001,      # Set your desired min_delta
            mode="auto",         # Set your desired mode
            verbose=1,           # Set the verbosity
            baseline=None,       # Set your baseline if needed
            restore_best_weights=False,  # Set to True if you want to restore best weights
            patience=30           # Set your desired patience
        )

    @property
    def _create_ckpt_callbacks(self):
        filepath = str(self.config.checkpoint_model_filepath)
        return tf.keras.callbacks.ModelCheckpoint(
            filepath=filepath,
            save_best_only=True
        )

    def get_tb_ckpt_callbacks(self):
        return [
            self._create_tb_callbacks,
            self._create_ckpt_callbacks,
            self._create_early_stopping_callback
        ]


