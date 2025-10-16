# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

import isaaclab.sim as sim_utils
from isaaclab.sensors.camera import TiledCameraCfg
from isaaclab.utils import configclass

from isaaclab_tasks.manager_based.manipulation.lift.config.franka.joint_pos_env_cfg import FrankaCubeLiftEnvCfg


@configclass
class FrankaCubeLiftEnvCameraCfg(FrankaCubeLiftEnvCfg):
    def __post_init__(self):
        super().__post_init__()

        # Disable debug visualization for object pose
        if hasattr(self.commands, "object_pose"):
            print("[INFO]: Disabling debug visualization for object pose")
            self.commands.object_pose.debug_vis = False
        else:
            print("[INFO]: No object pose found in environment configuration")

        self.episode_length_s = 2.0
        self.cam_width = 320
        self.cam_height = 240

        front_cam_cfg = TiledCameraCfg(
            prim_path="{ENV_REGEX_NS}/front_camera",
            update_period=0,
            height=self.cam_height,
            width=self.cam_width,
            data_types=["rgb"],
            debug_vis=True,
            offset=TiledCameraCfg.OffsetCfg(
                # pos=(0.0, 0.0, 2.5),  # Position above the cabinet (cabinet is at 0.8, 0, 0.4)
                # rot=(0.0, 0.7071, -0.7071, 0.0),  # -90° around Y axis for top-down view
                # rot=(1.0, 0.0, 0.0, 0.0),
                pos=(1.6, 0.0, 0.7),
                rot=(0.35355, -0.61237, -0.61237, 0.35355),
                convention="ros",
            ),
            spawn=sim_utils.PinholeCameraCfg(
                focal_length=24.0,
                focus_distance=400.0,
                horizontal_aperture=20.955,
                clipping_range=(0.1, 1e4),
            ),
        )

        setattr(self.scene, "front_camera", front_cam_cfg)

        wrist_cam_cfg = TiledCameraCfg(
            prim_path="/World/envs/env_.*/Robot/panda_hand/wrist_cam",
            update_period=0,
            height=self.cam_height,
            width=self.cam_width,
            debug_vis=True,
            data_types=["rgb"],
            offset=TiledCameraCfg.OffsetCfg(
                # pos=(0.06, 0.0, 0.0),
                # rot=(-0.70614, 0.03701, 0.03701, -0.70614), convention="ros"
                pos=(0.13, 0.0, -0.15),
                rot=(-0.70614, 0.03701, 0.03701, -0.70614),
                convention="ros",
                # rot=(1.0, 0.0, 0.0, 0.0),
            ),
            spawn=sim_utils.PinholeCameraCfg(
                focal_length=24.0,
                focus_distance=400.0,
                horizontal_aperture=20.955,
                clipping_range=(0.1, 1e4),
            ),
        )
        setattr(self.scene, "wrist_camera", wrist_cam_cfg)


@configclass
class FrankaCubeLiftEnvCameraCfg_PLAY(FrankaCubeLiftEnvCameraCfg):
    def __post_init__(self):
        super().__post_init__()

        self.scene.num_envs = 4
        self.scene.env_spacing = 2.5
        # disable randomization for play
        self.observations.policy.enable_corruption = False
