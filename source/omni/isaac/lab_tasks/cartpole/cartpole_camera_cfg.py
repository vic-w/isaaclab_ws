"""Camera-augmented cartpole task configuration for Isaac Lab.

This module extends the default cartpole task configuration that ships with Isaac Lab
by attaching a camera sensor to the cart and wiring its RGB output into the policy
observation group.  The configuration can be registered under Hydra and consumed by
RL pipelines such as rl-games.  All numerical values are kept deliberately modest so
that the camera observations can be generated in real time on both workstation GPUs
and cloud instances.
"""

from __future__ import annotations

from dataclasses import field

from omni.isaac.lab.managers import ObservationGroupCfg, ObservationTermCfg
from omni.isaac.lab.sensors.camera import CameraCfg, CameraPropertiesCfg
from omni.isaac.lab.utils import configclass
from omni.isaac.lab.utils.math import euler_xyz_to_quat
from omni.isaac.lab_tasks.cartpole.cartpole_cfg import CartpoleTaskCfg, CartpoleTaskCfg_PLAY


_CAMERA_WIDTH = 84
_CAMERA_HEIGHT = 84
_CAMERA_RATE = 30.0


@configclass
class CartpoleCameraObservationsCfg(CartpoleTaskCfg.ObservationsCfg):
    """Observation configuration that exposes both proprioception and RGB data.

    The inherited cartpole configuration already provides a group named ``policy``
    that contains the joint position/velocity terms.  We clone that group so that
    the original proprioceptive observations remain untouched while we append a new
    term that reads the RGB image from the camera sensor registered below.
    """

    policy: ObservationGroupCfg = field(default_factory=lambda: CartpoleTaskCfg.ObservationsCfg.policy.clone())

    def __post_init__(self) -> None:
        super().__post_init__()

        # Enable the camera term on the cloned group.
        self.policy.terms["pole_camera_rgb"] = ObservationTermCfg(
            func="sensors.camera.rgb",  # Provided by the default camera observation pipeline
            params={"sensor": "pole_camera"},
            scale=1.0,
        )
        # Ensure the observation manager keeps the RGB values in the [0, 1] range and
        # skips the automatic clipping that is typically applied to proprioceptive signals.
        self.policy.enable_corruption(False)


@configclass
class CartpoleCameraSensorsCfg(CartpoleTaskCfg.SensorsCfg):
    """Attach a forward looking camera to the cartpole cart."""

    pole_camera: CameraCfg = CameraCfg(
        prim_path="{ENV_REGEX_NS}/Cartpole/pole_camera",
        update_period=1.0 / _CAMERA_RATE,
        history_length=1,
        data_types=["rgb"],
        spawn=CameraCfg.SpawnCfg(
            attach_yaw_only=False,
            parent_prim_path="{ENV_REGEX_NS}/Cartpole/root",
            translation=(0.0, -1.5, 0.8),
            orientation=euler_xyz_to_quat((0.0, 0.0, 0.0)),
            camera_props=CameraPropertiesCfg(
                width=_CAMERA_WIDTH,
                height=_CAMERA_HEIGHT,
                fov=60.0,
            ),
        ),
    )


@configclass
class CartpoleCameraTaskCfg(CartpoleTaskCfg):
    """Cartpole task with an RGB camera exposed through the observation manager."""

    observations: CartpoleCameraObservationsCfg = CartpoleCameraObservationsCfg()
    sensors: CartpoleCameraSensorsCfg = CartpoleCameraSensorsCfg()


@configclass
class CartpoleCameraTaskCfg_PLAY(CartpoleTaskCfg_PLAY, CartpoleCameraTaskCfg):
    """Play configuration that mirrors the RGB observations during evaluation."""

    pass
