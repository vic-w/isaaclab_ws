# Isaac Lab Cartpole Camera Task

This repository provides an Isaac Lab reinforcement-learning task that extends the
default cartpole example with an RGB camera.  The task configuration attaches the
camera to the cart, adds the pixel observations to the policy input, and ships with
an ``rl-games`` training recipe that uses a convolutional encoder for the image
stream.

## Repository layout

- ``source/omni/isaac/lab_tasks/cartpole/cartpole_camera_cfg.py`` — Python module that
  defines the camera-augmented task configuration using Isaac Lab's config dataclasses.
- ``config/task/rl/cartpole_camera.yaml`` — Hydra/``rl-games`` configuration that wires
  the new task into the existing cartpole training pipeline while enabling a CNN-based
  encoder for the RGB observations.
- ``scripts`` — Placeholder for launch/training scripts.  Training is typically run via
  Isaac Lab's ``python scripts/rlgames_train.py --task=cartpole_camera`` command once
  this repository is installed as an Isaac Lab package.

## Usage

1. Install Isaac Lab and its dependencies following the official documentation.
2. Add this workspace to the Python path, for example with ``pip install -e .``.
3. Launch training with ``python scripts/rlgames_train.py --task cartpole_camera`` from
   your Isaac Lab checkout.  The ``rl-games`` policy will now receive the camera image
   tensor named ``pole_camera_rgb`` in addition to the original proprioceptive signals.

Refer to the inline comments inside the configuration module for the specific camera
placement and observation wiring details.
