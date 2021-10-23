from collections import OrderedDict
import os
import argparse
import json
import time

from rescale_tiffs import rescale_tiffs
from auto_contrast_tiffs import auto_contrast_tiffs
from section_tiffs import section_tiffs
from run_soax import run_soax
from snakeutils.logger import RecordLogger, PrintLogger
from convert_snakes_to_json import convert_snakes_to_json
from join_sectioned_snakes import join_sectioned_snakes
from make_orientation_fields import make_orientation_fields
from sindy_matrices_from_snakes import sindy_matrices_from_snakes
from bead_piv import bead_piv
from tube_piv import tube_piv
from create_soax_param_files import create_soax_param_files

from setup_app import (
    SoaxSetupApp,
    RescaleSetupForm,
    AutoContrastSetupForm,
    SectioningSetupForm,
    SoaxParamsSetupPage1Form,
    SoaxParamsSetupPage2Form,
    SoaxParamsSetupPage3Form,
    SoaxParamsSetupPage4Form,
    SoaxRunSetupForm,
    SnakesToJsonSetupForm,
    JoinSectionedSnakesSetupForm,
    MakeOrientationFieldsSetupForm,
    BeadPIVSetupForm,
    TubePIVSetupForm,
)

def perform_action(action_name, setting_strings, make_dirs, logger):
    if action_name == "rescale_tiffs":
        parsed_rescale_tiffs_settings = RescaleSetupForm.parseSettings(setting_strings, make_dirs)
        rescale_tiffs(
            parsed_rescale_tiffs_settings["source_tiff_dir"],
            parsed_rescale_tiffs_settings["target_tiff_dir"],
            parsed_rescale_tiffs_settings["input_dims"],
            parsed_rescale_tiffs_settings["output_dims"],
            logger=logger,
        )
    elif action_name == "auto_contrast_tiffs":
        parsed_auto_contrast_settings = AutoContrastSetupForm.parseSettings(setting_strings, make_dirs)
        auto_contrast_tiffs(
            parsed_auto_contrast_settings["source_tiff_dir"],
            parsed_auto_contrast_settings["target_tiff_dir"],
            parsed_auto_contrast_settings["max_cutoff_percent"],
            parsed_auto_contrast_settings["min_cutoff_percent"],
            parsed_auto_contrast_settings["workers_num"],
            logger=logger,
        )
    elif action_name == "section_tiffs":
        parsed_sectioning_settings = SectioningSetupForm.parseSettings(setting_strings, make_dirs)
        section_tiffs(
            parsed_sectioning_settings["section_max_size"],
            parsed_sectioning_settings["source_tiff_dir"],
            parsed_sectioning_settings["target_sectioned_tiff_dir"],
            parsed_sectioning_settings["workers_num"],
            logger=logger,
        )
    elif action_name == "create_soax_param_files":
        parsed_page1_params_settings = SoaxParamsSetupPage1Form.parseSettings(setting_strings, make_dirs)
        parsed_page2_params_settings = SoaxParamsSetupPage2Form.parseSettings(setting_strings, make_dirs)
        parsed_page3_params_settings = SoaxParamsSetupPage3Form.parseSettings(setting_strings, make_dirs)
        parsed_page4_params_settings = SoaxParamsSetupPage4Form.parseSettings(setting_strings, make_dirs)

        parsed_params_settings = {
            **parsed_page1_params_settings,
            **parsed_page2_params_settings,
            **parsed_page3_params_settings,
            **parsed_page4_params_settings,
        }

        create_soax_param_files(
            target_dir=parsed_params_settings["params_save_dir"],
            init_z=parsed_params_settings["init_z"],
            damp_z=parsed_params_settings["damp_z"],
            intensity_scaling_start_stop_step=parsed_params_settings["intensity_scaling"],
            gaussian_std_start_stop_step=parsed_params_settings["gaussian_std"],
            ridge_threshold_start_stop_step=parsed_params_settings["ridge_threshold"],
            maximum_foreground_start_stop_step=parsed_params_settings["maximum_foreground"],
            minimum_foreground_start_stop_step=parsed_params_settings["minimum_foreground"],
            snake_point_spacing_start_stop_step=parsed_params_settings["snake_point_spacing"],
            min_snake_length_start_stop_step=parsed_params_settings["min_snake_length"],
            maximum_iterations_start_stop_step=parsed_params_settings["maximum_iterations"],
            change_threshold_start_stop_step=parsed_params_settings["change_threshold"],
            check_period_start_stop_step=parsed_params_settings["check_period"],
            alpha_start_stop_step=parsed_params_settings["alpha"],
            beta_start_stop_step=parsed_params_settings["beta"],
            gamma_start_stop_step=parsed_params_settings["gamma"],
            external_factor_start_stop_step=parsed_params_settings["external_factor"],
            stretch_factor_start_stop_step=parsed_params_settings["stretch_factor"],
            number_of_background_radial_sectors_start_stop_step=parsed_params_settings["number_of_background_radial_sectors"],
            background_z_xy_ratio_start_stop_step=parsed_params_settings["background_z_xy_ratio"],
            radial_near_start_stop_step=parsed_params_settings["radial_near"],
            radial_far_start_stop_step=parsed_params_settings["radial_far"],
            delta_start_stop_step=parsed_params_settings["delta"],
            overlap_threshold_start_stop_step=parsed_params_settings["overlap_threshold"],
            grouping_distance_threshold_start_stop_step=parsed_params_settings["grouping_distance_threshold"],
            grouping_delta_start_stop_step=parsed_params_settings["grouping_delta"],
            minimum_angle_for_soac_linking_start_stop_step=parsed_params_settings["minimum_angle_for_soac_linking"],
            logger=logger,
        )
    elif action_name == "run_soax":
        parsed_soax_run_settings = SoaxRunSetupForm.parseSettings(setting_strings, make_dirs)

        run_soax(
            parsed_soax_run_settings["batch_soax_path"],
            parsed_soax_run_settings["source_tiff_dir"],
            parsed_soax_run_settings["param_files_dir"],
            parsed_soax_run_settings["target_snakes_dir"],
            parsed_soax_run_settings["soax_log_dir"],
            parsed_soax_run_settings["use_subdirs"],
            parsed_soax_run_settings["workers"],
            logger=logger,
        )
    elif action_name == "convert_snakes_to_json":
        parsed_snakes_to_json_settings = SnakesToJsonSetupForm.parseSettings(setting_strings, make_dirs)

        convert_snakes_to_json(
            parsed_snakes_to_json_settings["source_snakes_dir"],
            parsed_snakes_to_json_settings["target_json_dir"],
            parsed_snakes_to_json_settings["source_snakes_depth"],
            parsed_snakes_to_json_settings["offset_pixels"],
            parsed_snakes_to_json_settings["dims_pixels"],
            parsed_snakes_to_json_settings["pixel_spacings_um_xyz"],
            logger=logger,
        )
    elif action_name == "join_sectioned_snakes":
        parsed_join_sectioned_snakes_settings = JoinSectionedSnakesSetupForm.parseSettings(setting_strings, make_dirs)

        join_sectioned_snakes(
            parsed_join_sectioned_snakes_settings["source_json_dir"],
            parsed_join_sectioned_snakes_settings["target_json_dir"],
            source_jsons_depth=parsed_join_sectioned_snakes_settings["source_jsons_depth"],
            logger=logger,
        )
    elif action_name == "make_orientation_fields":
        parsed_make_orientation_fields_settings = MakeOrientationFieldsSetupForm.parseSettings(setting_strings, make_dirs)

        make_orientation_fields(
            parsed_make_orientation_fields_settings["source_json_dir"],
            parsed_make_orientation_fields_settings["target_data_dir"],
            parsed_make_orientation_fields_settings["source_jsons_depth"],
            parsed_make_orientation_fields_settings["image_width"],
            parsed_make_orientation_fields_settings["image_height"],
            logger=logger,
        )
    elif action_name == "make_sindy_matrices_from_snakes":
        parsed_make_sindy_matrices_from_snakes_settings = MakeSindyMatricesFromSnakesSetupForm.parseSettings(setting_strings, make_dirs)

        make_sindy_matrices_from_snakes(
            parsed_make_sindy_matrices_from_snakes_settings["source_json_dir"],
            parsed_make_sindy_matrices_from_snakes_settings["source_jsons_depth"],
            parsed_make_sindy_matrices_from_snakes_settings["orientation_matrix_dir"],
            parsed_make_sindy_matrices_from_snakes_settings["position_matrix_dir"],
            logger=logger,
        )
    elif action_name == "do_bead_PIV":
        parsed_bead_PIV_settings = BeadPIVSetupForm.parseSettings(setting_strings, make_dirs)

        bead_piv(
            parsed_bead_PIV_settings["source_tiff_dir"],
            parsed_bead_PIV_settings["tiff_fn_letter_before_frame_num"],
            parsed_bead_PIV_settings["target_piv_data_dir"],
            parsed_bead_PIV_settings["x_y_pixel_size_um"],
            parsed_bead_PIV_settings["z_stack_spacing_um"],
            parsed_bead_PIV_settings["bead_diameter_um"],
            logger=logger,
        )
    elif action_name == "do_tube_PIV":
        parsed_tube_PIV_settings = TubePIVSetupForm.parseSettings(setting_strings, make_dirs)

        tube_piv(
            parsed_tube_PIV_settings["source_tiff_dir"],
            parsed_tube_PIV_settings["target_piv_data_dir"],
            logger=logger,
        )
    else:
        raise Exception("Unknown action name '{}'".format(action_name))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Soax Helper')
    parser.add_argument('--load-settings',default=None,help="Skip GUI, Run from settings loaded from JSON file")
    parser.add_argument('--save-settings',default=None,help="Save settings from GUI menu to JSON file")
    parser.add_argument('--do-not-run', default=False, action='store_true', help='Will load or save settings but will not run. Use if you want to just create settings but not run them')
    parser.add_argument('--make-dirs',default=False,action='store_true', help='If --load_settings, whether program should make directories in settings file is the directories don\'t exist already.')

    args = parser.parse_args()
    if args.load_settings is not None and args.save_settings is not None:
        raise Exception("Loading settings and saving settings is not supported"
            "(loading tells program to skip GUI, but saving is meant to store "
            "settings configured in GUI)")
    if args.load_settings is not None:
        if not args.load_settings.endswith(".json"):
            raise Exception("Invalid settings load file '{}': must be json file".format(args.load_settings))

        if not os.path.exists(args.load_settings):
            raise Exception("File '{}' does not exist".format(args.load_settings))

        with open(args.load_settings, "r") as f:
            action_configs = json.load(f)
    else:
        if args.save_settings is not None:
            if not args.save_settings.endswith(".json"):
                raise Exception("Cannot save settings as '{}', file must have '.json' extension".format(args.save_settings))
            if os.path.exists(args.save_settings):
                raise Exception("Cannot save settings as '{}', already exists".format(args.save_settings))
        app = SoaxSetupApp(make_dirs=args.make_dirs)
        app.run()

        action_configs = app.getActionConfigs()

        if args.save_settings is not None:
            with open(args.save_settings, "w") as f:
                json.dump(action_configs, f, indent=4)

    if args.do_not_run:
        exit()

    all_loggers = []
    all_times = []

    for action_conf in action_configs:
        action_name = action_conf["action"]
        action_settings = action_conf["settings"]

        start_time = time.time()

        action_logger = RecordLogger()
        all_loggers.append((action_name, action_logger))

        perform_action(action_name, action_settings, args.make_dirs, action_logger)

        end_time = time.time()
        elapsed = end_time - start_time
        all_times.append((action_name, elapsed))
        PrintLogger.log("{} took {} seconds".format(action_name, elapsed))

    for step_name, record_logger in all_loggers:
        if len(record_logger.errors) > 0:
            PrintLogger.error("ERRORS FROM {}".format(step_name))
            for err in record_logger.errors:
                PrintLogger.error("  " + err)

    for i, (step_name, seconds_taken) in enumerate(all_times):
        print("Step #{}, '{}' took {} seconds".format(i + 1, step_name, seconds_taken))
