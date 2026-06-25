#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Anymaker Unlock — разблокировка предметов в Anymaker (Demo).

Кнопки/режимы:
  * Пропатчить — открывает контент. По умолчанию БЕЗОПАСНЫЙ набор
                 (tech_tier <= 2): не вызывает пасхалку с рыбой и не ломает сохранение.
  * Галочка «Полный анлок» — открывает ВООБЩЕ ВСЁ, включая контент полной игры
                 (tech_tier 3/4/5: военка, топ-оружие, спец-компоненты).
                 ВНИМАНИЕ: именно это включает пасхалку разработчиков —
                 рыбу вокруг головы и блокировку сохранения мира. Только для изучения.
  * Откатить — возвращает ваш исходный unlocks.txt из резервной копии.

При первом патче создаётся резервная копия unlocks.txt -> unlocks.txt.backup.
Откат всегда восстанавливает именно её.

Сборка в .exe (Windows):
    pip install pyinstaller
    python -m PyInstaller --onefile --windowed --name "Anymaker Unlock" anymaker_unlock_gui.py
"""

import os, json, shutil
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# ───────── встроенные списки ─────────
SAFE_ITEMS = ['overalls', 'hi_vis_overalls', 'fishing_boots', 'ski_beanie', 'ushanka', 'ushanka_open', 'beanie', 'cap', 'headlamp', 'adventure_hat', 'western_hat', 'straw_hat', 'park_ranger_hat', 'ski_mask', 'balaclava', 'mask', 'safety_goggles', 'safety_glasses', 'ski_trousers', 'jeans', 'joggers', 'shorts', 'trousers', 'walking_trousers', 'waterproof_leggings', 'chainsaw_trousers', 'scrubs_trousers', 'park_ranger_shorts', 'trousers_leg_bag', 'body_warmer', 'fleece', 'henley_top', 'hoodie', 'shirt', 'sweatshirt', 't_shirt', 'shirt_tucked_in', 'safari_shirt', 'hi_vis_vest', 'scrubs_shirt', 'park_ranger_shirt', 'park_ranger_shirt_tucked_in', 'waistcoat', 'western_waistcoat', 'polo_shirt', 'short_sleeve_shirt', 'short_sleeve_shirt_tucked_in', 'shirt_button_up', 'shirt_button_up_tucked_in', 'fishing_jacket', 'shoes', 'trainers', 'walking_boots', 'wellingtons', 'nurse_shoes', 'feet_covers', 'scarf', 'sling_shirt', 'fingerless_gloves', 'working_gloves', 'leather_gloves', 'chainsaw_gloves', 'driving_gloves', 'small_pouch', 'medium_pouch', 'disposable_coveralls', 'working_trousers', 'wheel_car', 'wheel_motorcycle', 'wheel_quadbike', 'vehicle_editor_add_component', 'vehicle_editor_add_building_component', 'vehicle_editor_paint', 'vehicle_editor_add_edge', 'vehicle_editor_add_plate', 'vehicle_editor_add_window', 'vehicle_editor_add_opening', 'vehicle_editor_add_hatch', 'vehicle_editor_remove', 'vehicle_editor_electric', 'vehicle_editor_mechanical', 'vehicle_editor_liquid', 'vehicle_editor_gas', 'vehicle_editor_belt', 'vehicle_editor_data', 'vehicle_editor_properties', 'vehicle_editor_duplicate', 'wheel_van', 'wheel_5_prong', 'wheel_5_prong_tread', 'wheel_rim_20', 'wheel_rim_20_tread', 'wheel_rim_22', 'wheel_rim_22_tread', 'wheel_rim_24', 'wheel_rim_24_tread', 'oil_filter', 'air_filter', 'wheel4x4', 'battery_a', 'battery_b', 'vehicle_editor_microcontroller', 'bandage', 'food_stew', 'tactical_knife', 'jerry_can', 'splint', 'adrenaline_auto_injector', 'painkillers', 'canteen', 'food_tuna', 'food_sardines', 'food_meat', 'food_unlabelled_a', 'food_unlabelled_b', 'food_unlabelled_c', 'food_canned_veg', 'food_soup', 'food_canned_milk', 'food_rice', 'food_canned_fruit', 'food_canned_bread', 'food_beans', 'food_water', 'food_preservatives', 'food_jam', 'food_coffee_grounds', 'food_cola', 'food_lemonade', 'axe', 'rope', 'penknife', 'radio_a', 'radio_b', 'torch', 'crate_a', 'crate_b', 'semi_automatic_pistol_hi_power', 'semi_automatic_pistol_hi_power_magazine', 'automatic_pistol', 'automatic_pistol_magazine', 'semi_automatic_pistol', 'semi_automatic_pistol_magazine', 'machine_pistol', 'machine_pistol_magazine', 'revolver_3', 'revolver_4', 'revolver_6', 'bolt_action_rifle', 'single_shot_shotgun_12_gauge', 'pump_action_shotgun', 'pump_action_shotgun_tactical', 'chemlight', 'angle_flashlight', 'flare', 'grenade_smoke', 'pistol_holster', 'tatical_knife_holster', '9mm_ammo_box', '357_magnum_ammobox', '45_ammo_box', '308_rifle_ammo_box', '12_gauge_shotgun_cartridges_ammobox', 'bag_school_backpack', 'bag_24_7_rucsac', 'bag_guide_45_short', 'bag_tactical_ranger_24l', 'water_container', 'oil_container', 'vehicle_editor_temperature', 'vehicle_editor_weld', 'direction_finder', 'battery_cell', 'vehicle_editor_repair', 'game_manual', 'insignia_patch_1_1', 'insignia_patch_1_2', 'insignia_patch_2_1', 'insignia_patch_2_2', 'insignia_patch_3_1', 'insignia_patch_3_2', 'insignia_patch_4_1', 'insignia_patch_4_2', 'smoke_discharger_grenade', 'first_aid_kit', 'vehicle_editor_hydraulic', 'vehicle_editor_add_edge_2']

SAFE_COMP_REGULAR = ['engine', 'gearbox', 'engine_wheel', 'liquid_tank', 'radiator', 'wheel', 'gear_track', 'drive_shaft', 'battery_a', 'bench_seat', 'round_headlight_a', 'round_headlight_b', 'round_headlight_c', 'winch', 'square_headlight', 'handle', 'rope_hook_point', 'tool_wall', 'steering_wheel', 'high_back_car_seat', 'low_back_car_seat', 'v_engine', 'opposed_engine', 'throttle_collective', 'throttle', 'multi_throttle', 'trim_throttle', 'beacon_light', 'light_bar', 'siren_light', 'oil_filter', 'tow_bar', 'tow_hitch', 'differential_gearbox_a', 'button_push', 'button_push_round', 'button_push_round_on', 'button_push_round_off', 'turnable_knob_a', 'turnable_knob_b', 'turnable_knob_c', 'turnable_knob_d', 'turnable_knob_e', 'circular_dial_a', 'circular_dial_small_a', 'circular_dial_b', 'slider', 'additive_button_a', 'additive_button_b', 'light_indicator_a', 'light_indicator_b', 'light_indicator_c', 'light_indicator_round_a', 'light_indicator_round_b', 'additive_round_button', 'additive_round_button_alt', 'light_indicator_bulb', 'light_indicator_arrow_a', 'light_indicator_arrow_b', 'square_button_on', 'square_button_off', 'square_button_arrows', 'square_button_arrow', 'square_button_square', 'square_button_circle', 'round_button_arrows', 'round_button_arrow', 'round_button_square', 'round_button_circle', 'switch', 'key_switch', 'toggle_switch', 'toggle_switch_cover', 'emergency_stop_button_a', 'emergency_stop_button_b', 'circuit_breaker', 'circular_dial_small_b', 'circular_dial_small_c', 'circular_dial_small_d', 'circular_dial_c', 'circular_dial_d', 'circular_dial_e', 'circular_dial_f', 'circular_dial_g', 'circular_dial_h', 'alternator_motor', 'hinge_pin', 'tyre_mount', 'latch_handle', 'rail_ballscrew', 'actuator_stepper_motor', 'latch_pin', 'latch_knuckle', 'electric_motor_a', 'electric_motor_b', 'catalytic', 'angle_bracket', 'handbrake', 'drive_shaft_b', 'gear_stick', 'rail', 'rail_slider', 'rail_ballscrew_slider', 'liquid_pump', 'hinge_knuckle', 'mounting_pin', 'mounting_knuckle', 'differential_gearbox_b', 'pulley_wheel', 'liquid_port_straight', 'liquid_port_angle', 'mechanical_interface_out_straight', 'electrical_interface_straight', 'gas_port_straight', 'gas_pump', 'exhaust_manifold_angle', 'air_manifold', 'exhaust_manifold_straight', 'fuel_manifold', 'oil_manifold', 'coolant_manifold', 'battery_b', 'electric_port_straight', 'electric_port_angle', 'torque_interface_straight', 'gas_interface_straight', 'liquid_interface_straight', 'mechanical_bracket', 'electric_bracket', 'electric_junction', 'junction_x_liquid_pipe_a', 'junction_t_liquid_pipe_a', 'junction_x_gas_pipe_a', 'junction_t_gas_pipe_a', 'mechanical_junction', 'mechanical_junction_abs', 'mechanical_junction_invert', 'mechanical_junction_max', 'mechanical_junction_min', 'mechanical_junction_offset', 'mechanical_junction_scale', 'mechanical_junctions_set_reset', 'mechanical_junction_toggle', 'electric_relay', 'square_bracket', 'mechanical_junction_add', 'gas_vent', 'liquid_vent', 'liquid_bracket', 'gas_bracket', 'gas_tank_a', 'gas_tank_b', 'gas_tank_c', 'mechanical_interface_in_straight', 'electrical_interface_angle', 'gas_interface_angle', 'liquid_interface_angle', 'torque_interface_angle', 'mechanical_interface_in_angle', 'mechanical_interface_out_angle', 'gas_port_angle', 'liquid_fill_port', 'liquid_pressure_sensor', 'gas_pressure_sensor', 'liquid_temperature_sensor', 'gas_temperature_sensor', 'liquid_valve_straight', 'liquid_valve_t', 'gas_valve_straight', 'gas_valve_t', 'mechanical_handle', 'clutch', 'gearbox_fixed_ratio', 'weight_block', 'short_shifter', 'radiator_fan_a', 'lever_switch_curve_a', 'lever_switch_a', 'lever_switch_b', 'pulley_a', 'pulley_straight_a', 'pulley_corner_a', 'acceleration_sensor', 'tilt_sensor', 'compass_sensor', 'gyro_rotation_sensor']

SAFE_COMP_BUILDING = ['chair_a', 'chair_b', 'deckchair_a', 'stool_a', 'toilet_a', 'sink_a', 'bath_a', 'pouffe_a', 'pouffe_b', 'sofa_a', 'armchair_a', 'sofa_b', 'sofa_c', 'wardrobe_a', 'wardrobe_b', 'side_table_a', 'side_table_b', 'side_table_c', 'tv_a', 'tv_b', 'table_a', 'table_b', 'lamp_a', 'lamp_b', 'book_shelf_a', 'book_shelf_b', 'desk_a', 'coffee_table_a', 'record_cube_a', 'bed_a', 'bed_b', 'king_bed_a', 'king_bed_b', 'washer_a', 'dryer_a', 'fridge_a', 'cooker_a', 'filing_cabinet_a', 'paper_bin_a', 'trashcan_b', 'work_cubical_b', 'work_cubical_a', 'work_desk_a', 'police_desk_a', 'interrogation_desk_a', 'vending_machine_a', 'letter_sorter_a', 'office_cabinet_a', 'watercooler_a', 'filing_cabinet_b', 'chair_d', 'fan_a', 'printer_a', 'break_room_table_a', 'cleaning_dolly_a', 'wet_floor_sign_a', 'desk_chair_a', 'desk_chair_b', 'chair_c', 'whiteboard_a', 'line_barricade_a', 'barricade_a', 'hose_reel_a', 'hose_pump_a', 'cone_a', 'office_cabinet_b', 'locker_a', 'locker_b', 'locker_c', 'bench_a', 'bench_b', 'store_shelves_a', 'store_shelves_b', 'store_shelves_c', 'till_a', 'trolly_a', 'drinks_cooler_a', 'store_freezer_a', 'convenience_till_a', 'doctors_bed_a', 'autopsy_table_a', 'autopsy_sink_a', 'surgical_trolly_a', 'paper_bin_b', 'doctor_desk_a', 'hospital_bed_a', 'hospital_bed_b', 'hospital_divider_a', 'hospital_divider_b', 'waiting_seats_a', 'nurses_trolly_a', 'sainitizer_a', 'anesthesia_machine_a', 'medical_waste_a', 'baby_bed_a', 'baby_incubator_a', 'defibrillator_b', 'defibrillator_a', 'heart_monitor_a', 'iv_drip_a', 'ecg_a', 'medical_gas_tank_b', 'medical_gas_tank_a', 'blood_pressure_a', 'wheelchair_a', 'surgical_light_a', 'shelving_a', 'shelving_b', 'shelving_c', 'lumber_shelving_b', 'lumber_shelving_a', 'shelving_d', 'storage_box_f', 'storage_box_e', 'pallet_a', 'pallet_b', 'storage_box_g', 'storage_box_b', 'storage_box_a', 'storage_box_d', 'storage_box_c', 'tool_cabinet_a', 'barrel_b', 'barrel_a', 'storage_holder_a', 'wearhouse_dolly_a', 'barrier_a', 'storage_sack_a', 'hangar_dolly_a', 'chainsaw_jig', 'saw_setup_a', 'water_tank_a', 'pallet_jack_a', 'fuel_tank_a', 'hand_trucks_a', 'hangar_fan_a', 'doctor_cabinet_a', 'workshop_cabinet_a', 'log_deck_a', 'log_conveyor_a', 'wooden_planks_a', 'covered_planks_a', 'posts_a', 'covered_planks_b', 'saw_a', 'ladder_a', 'bar_a', 'pool_table_a', 'jukebox_a', 'restaurant_table_d', 'chair_f', 'chair_g', 'stool_d', 'restaurant_table_c', 'restaurant_table_e', 'restaurant_table_b', 'restaurant_table_a', 'stool_c', 'diner_chair_a', 'diner_table_b', 'booth_c', 'booth_b', 'booth_a', 'diner_table_a', 'restaurant_fridge_a', 'fryer_a', 'cooking_storage_a', 'restaurant_grill_a', 'restaurant_oven_a', 'restaurant_range_a', 'restaurant_range_b', 'tray_return_a', 'restaurant_trolly_a', 'restaurant_sink_a', 'restaurant_bin_a', 'hotel_bed_set_a', 'hotel_bed_a', 'hotel_chair_a', 'hotel_coffetable_a', 'hotel_coffetable_b', 'hotel_desk_a', 'hotel_side_tv_a', 'ice_machine_a', 'hotel_counter_a', 'laundry_trolley_a', 'minifridge_a', 'hotel_cleaning_dolly_a', 'luggage_trolley_a', 'hotel_dresser_a', 'hotel_bed_pouffe_a', 'hotel_storage_grid_a', 'bleachers_a', 'basketball_net_a', 'science_lab_cabinet_a', 'school_coat_hooks_a', 'tv_av_set_a', 'school_draws_a', 'cubed_shelves_b', 'school_computer_a', 'book_shelf_c', 'teachers_desk_a', 'stool_b', 'vaulting_buck_a', 'book_shelf_d', 'vaulting_buck_b', 'science_lab_table_a', 'chalkboard_a', 'projector_a', 'trashcan_a', 'school_chair_a', 'school_desk_a', 'church_organ_a', 'church_chair_a', 'chair_e', 'confessional_a', 'church_pew_a', 'church_alter_a', 'church_desk_a', 'church_alter_b', 'church_basin_a', 'hotel_bedside_a', 'cooler_unit_a', 'ac_unit_a', 'portable_sign_a', 'gas_pump_a', 'rooftop_satellite_a', 'door_lamp_a', 'tap_a', 'hose_a', 'sign_shop_a', 'sign_shop_b', 'sign_shop_c', 'lab_table_a', 'lab_table_b', 'lab_table_c', 'lab_robot_arm_a', 'lab_standing_autoclave_a', 'lab_centrifuge_a', 'lab_automated_analyser_a', 'lab_chemistry_diagnostics_machine_a', 'lab_fridge_a', 'lab_fridge_b', 'metal_bandsaw_a', 'metal_lathe_a', 'metal_milling_machine_a', 'workshop_desk_a', 'workshop_desk_b']

FULL_ITEMS = ['overalls', 'hi_vis_overalls', 'flying_suit', 'motorcyclist_leather_suit', 'driving_leather_suit', 'hazmat_type_c', 'hazmat_type_b', 'fishing_boots', 'military_helmet', 'combat_helmet', 'ski_beanie', 'ushanka', 'ushanka_open', 'beanie', 'cap', 'headband', 'fire_fighter_helmet', 'safety_helmet', 'headlamp', 'scrubs_hat', 'face_shield', 'pilot_hat', 'raf_helmet', 'raf_helmet_c_type', 'motorcyclist_helmet', 'gas_mask_full_face', 'gas_mask', 'adventure_hat', 'western_hat', 'straw_hat', 'chef_hat', 'chef_skullcap', 'top_hat', 'bowler_hat', 'beret', 'welding_mask', 'park_ranger_hat', 'side_cap', 'racing_helmet', 'ski_mask', 'balaclava', 'mask', 'military_sunglasses', 'aviator_sunglasses', 'safety_goggles', 'safety_glasses', 'military_trousers', 'ski_trousers', 'jeans', 'joggers', 'shorts', 'trousers', 'walking_trousers', 'waterproof_leggings', 'military_trousers_kneepads', 'military_trousers_drop_leg_bag', 'fire_fighter_trousers', 'fire_fighter_padded_trousers', 'chainsaw_trousers', 'scrubs_trousers', 'motorcyclist_leather_trousers', 'park_ranger_shorts', 'trousers_leg_bag', 'military_rain_coat', 'military_shirt', 'military_shirt_sleeves', 'military_shirt_tucked_in_a', 'military_shirt_tucked_in_b', 'military_vest', 'military_vest_tucked_in', 'body_warmer', 'fleece', 'henley_top', 'hoodie', 'shirt', 'sweatshirt', 't_shirt', 'shirt_tucked_in', 'military_coat', 'safari_shirt', 'fire_fighter_jacket', 'hi_vis_jacket', 'hi_vis_coat', 'hi_vis_vest', 'scrubs_shirt', 'doctors_coat', 'pilot_shirt', 'pilot_shirt_tucked_in', 'pilot_blazer', 'motorcyclist_leather_jacket', 'park_ranger_shirt', 'park_ranger_shirt_tucked_in', 'waistcoat', 'western_waistcoat', 'blazer_and_tie', 'polo_shirt', 'short_sleeve_shirt', 'short_sleeve_shirt_tucked_in', 'shirt_button_up', 'shirt_button_up_tucked_in', 'military_plate_vest', 'microphone_ptt', 'headset_ptt', 'helmet_light', 'military_strobe_light', 'safety_helmet_visor', 'fishing_jacket', 'military_backpack', 'military_boots', 'shoes', 'trainers', 'walking_boots', 'wellingtons', 'fire_fighter_boots', 'nurse_shoes', 'motorcylist_boots', 'hazmat_boots', 'feet_covers', 'western_boots', 'scarf', 'military_mask', 'neck_gaiter', 'sling_shirt', 'ear_defenders', 'military_gloves', 'arctic_gloves', 'fingerless_gloves', 'fire_fighter_gloves', 'working_gloves', 'leather_gloves', 'chainsaw_gloves', 'driving_gloves', 'small_pouch', 'medium_pouch', 'disposable_coveralls', 'working_trousers', 'wheel_car', 'wheel_truck', 'wheel_motorcycle', 'wheel_quadbike', 'vehicle_editor_add_component', 'vehicle_editor_add_building_component', 'vehicle_editor_paint', 'vehicle_editor_add_edge', 'vehicle_editor_add_plate', 'vehicle_editor_add_window', 'vehicle_editor_add_opening', 'vehicle_editor_add_hatch', 'vehicle_editor_remove', 'vehicle_editor_electric', 'vehicle_editor_mechanical', 'vehicle_editor_liquid', 'vehicle_editor_gas', 'vehicle_editor_belt', 'vehicle_editor_data', 'vehicle_editor_properties', 'vehicle_editor_duplicate', 'wheel_helicopter', 'wheel_plane', 'wheel_van', 'wheel_5_prong', 'wheel_5_prong_tread', 'wheel_rim_20', 'wheel_rim_20_tread', 'wheel_rim_22', 'wheel_rim_22_tread', 'wheel_rim_24', 'wheel_rim_24_tread', 'oil_filter', 'air_filter', 'wheel_truck_out_a', 'wheel_truck_out_b', 'wheel_truck_in_a', 'wheel_truck_in_b', 'wheel4x4', 'battery_a', 'battery_b', 'wheel_construction', 'vehicle_editor_microcontroller', 'wheel_tractor_a', 'wheel_tractor_b', 'wheel_construction_lws', 'wheel_loader', 'wheel_earthmover', 'wheel_heavyloader', 'bandage', 'food_stew', 'antibiotics', 'tactical_knife', 'jerry_can', 'saline_bag', 'blood_bag', 'plasma_bag', 'splint', 'suture_kit', 'antiseptic_spray', 'morphine_auto_injector', 'adrenaline_auto_injector', 'surgical_skin_glue', 'painkillers', 'strong_painkillers', 'tourniquet', 'canteen', 'canteen_covered', 'food_tuna', 'food_sardines', 'food_meat', 'food_unlabelled_a', 'food_unlabelled_b', 'food_unlabelled_c', 'food_canned_veg', 'food_soup', 'food_canned_milk', 'food_rice', 'food_canned_fruit', 'food_canned_bread', 'food_beans', 'food_water', 'food_preservatives', 'food_jam', 'food_coffee_grounds', 'food_cola', 'food_lemonade', 'cooking_oil', 'food_salt', 'anti_nausea_tablets', 'spoon', 'lighter', 'utility_camping_mug', 'utility_bottle_opener', 'utility_can_opener', 'utility_camping_stove', 'axe', 'sleeping_bag', 'helmet_pouch', 'pocket_pouch', 'penknife_pouch', 'loose_pouch', 'medium_pouch_b', 'medium_pouch_c', 'molle_pouch', 'belt_pouch_a', 'belt_pouch_b', 'belt_pouch_c', 'sere_pouch_a', 'sere_pouch_b', 'sere_pouch_c', 'medium_pouch_d', 'night_vision_goggles', 'backpack_pouch', 'rope', 'penknife', 'medium_pouch_e', 'large_pouch', 'radio_a', 'radio_b', 'radio_ptt', 'machete', 'binoculars', 'torch', 'crate_a', 'crate_b', 'crate_c', 'semi_automatic_pistol_hi_power', 'semi_automatic_pistol_hi_power_magazine', 'automatic_pistol', 'automatic_pistol_magazine', 'semi_automatic_pistol', 'semi_automatic_pistol_magazine', 'machine_pistol', 'machine_pistol_magazine', 'submachine_gun_45', 'submachine_gun_45_magazine', 'rifle_short_barrel', 'rifle_long_barrel', 'revolver_3', 'revolver_4', 'revolver_6', 'bolt_action_sniper_rifle', 'bolt_action_sniper_rifle_magazine', 'rifle_magazine', 'battle_rifle', 'battle_rifle_magazine', 'mg_3', 'mg_3_magazine', 'submachine_gun_k_pdw', 'submachine_gun_a3', 'submachine_gun_a3_tactical', 'submachine_gun_a4', 'submachine_gun_sd', 'submachine_gun_magazine', 'assault_rifle_107', 'assault_rifle_107_magazine', 'bolt_action_rifle', 'single_shot_shotgun_12_gauge', 'pump_action_shotgun', 'pump_action_shotgun_tactical', 'light_machine_gun_m1', 'light_machine_gun_sa', 'light_machine_gun_magazine', 'rifle_a3', 'squad_automatic_weapon', 'general_purpose_machine_gun', 'los_missile_system', 'infrared_missile_command_system', 'm2', 'grenade_launcher', 'minigun', 'machine_pistol_silencer', 'machine_pistol_reflex_sight', 'machine_pistol_torch', 'night_vision_clip_on_long_range', 'aperture_sight', 'foldable_peep_sight', 'foldable_peep_sight_front', 'peep_sight', 'laser_sight', 'rifle_silencer', 'tactical_torch', 'night_vision_clip_on', 'holo_sight', 'hhs_magnifier', 'rifle_scope_5_25x56', 'red_dot_sight', 'rifle_scope_1_6x26_ffp', 'dual_role_optical_sight', 'thermal_clip_on_long_range', 'thermal_clip_on', 'squad_automatic_weapon_magazine', 'rifle_a3_magazine', 'chemlight', 'angle_flashlight', 'flare', 'grenade_smoke', 'grenade_flash', 'grenade_frag', 'grenade_frag_m67', 'machete_sheath', 'pistol_holster', 'pouch_ammo_pistol', 'pouch_ammo', 'pouch_ammo_x2', 'tatical_knife_holster', 'rifle_front_handle', '9mm_ammo_box', '357_magnum_ammobox', '45_ammo_box', '556_rifle_ammo_box', '762_rifle_ammo_box', '308_rifle_ammo_box', '12_gauge_shotgun_cartridges_ammobox', '40_53mm_grenade', '120_570mm_shell', 'infrared_missile_launch_assembly', 'disposable_gloves', 'headset', 'bag_school_backpack', 'bag_24_7_rucsac', 'bag_guide_45_short', 'bag_guide_45', 'bag_tactical_ranger_24l', 'bag_tactical_ranger_55l', 'bag_tactical_ranger_60l', 'bag_tactical_ranger_37l', 'water_container', 'oil_container', 'vehicle_editor_temperature', 'vehicle_editor_weld', 'general_purpose_machine_gun_magazine', 'direction_finder', 'battery_cell', 'vehicle_editor_repair', 'game_manual', '40_365mm_shell', 'insignia_patch_1_1', 'insignia_patch_1_2', 'insignia_patch_2_1', 'insignia_patch_2_2', 'insignia_patch_3_1', 'insignia_patch_3_2', 'insignia_patch_4_1', 'insignia_patch_4_2', 'ammo_can_m2', 'ammo_can_grenade_launcher', 'ammo_can_minigun', 'smoke_discharger_grenade', 'first_aid_kit', 'blade_rotor', 'blade_prop', 'vehicle_editor_hydraulic', 'vehicle_editor_add_edge_2', 'air_filter_b', 'keycard', 'fuse', 'frequency_cartridge']

FULL_COMP_REGULAR = ['engine', 'gearbox', 'engine_wheel', 'liquid_tank', 'radiator', 'wheel', 'gear_track', 'drive_shaft', 'battery_a', 'bench_seat', 'round_headlight_a', 'round_headlight_b', 'round_headlight_c', 'winch', 'klaxon', 'square_headlight', 'handle', 'horn_speaker', 'rope_hook_point', 'side_mirror', 'tool_wall', 'antenna_a', 'antenna_b', 'antenna_c', 'tool_box_a', 'tool_box_b', 'steering_wheel', 'high_back_car_seat', 'low_back_car_seat', 'v_engine', 'opposed_engine', 'flight_seat', 'throttle_collective', 'landing_gear', 'radial_engine', 'turbofan', 'throttle', 'multi_throttle', 'trim_throttle', 'pintle_mount', 'aileron', 'control_flap', 'beacon_light', 'light_bar', 'siren_light', 'truck_hitch', 'truck_hitch_kingpin', 'turbo', 'oil_filter', 'fighter_jet_throttle', 'retractable_landing_gear_side', 'retractable_landing_gear_front', 'tow_bar', 'tow_hitch', 'differential_gearbox_a', 'engine_block_b', 'engine_block_c', 'gearbox_b', 'gearbox_c', 'ejection_seat', 'button_push', 'button_push_round', 'button_push_round_on', 'button_push_round_off', 'turnable_knob_a', 'turnable_knob_b', 'turnable_knob_c', 'turnable_knob_d', 'turnable_knob_e', 'circular_dial_a', 'circular_dial_small_a', 'circular_dial_b', 'slider', '7_segment_lcd_display_1', '7_segment_lcd_display_3', '7_segment_lcd_display_7', '7_segment_lcd_display_backlight_1', '7_segment_lcd_display_backlight_3', '7_segment_lcd_display_backlight_7', 'additive_button_a', 'additive_button_b', 'led_strip', 'led_strip_short', 'spotted_led_strip', 'light_indicator_a', 'light_indicator_b', 'light_indicator_c', 'light_indicator_round_a', 'light_indicator_round_b', 'additive_round_button', 'additive_round_button_alt', 'speaker_a', 'speaker_b', 'speaker_c', 'light_indicator_bulb', 'light_indicator_arrow_a', 'light_indicator_arrow_b', 'square_button_on', 'square_button_off', 'square_button_arrows', 'square_button_arrow', 'square_button_square', 'square_button_circle', 'round_button_arrows', 'round_button_arrow', 'round_button_square', 'round_button_circle', 'switch', 'key_switch', 'toggle_switch', 'toggle_switch_cover', 'emergency_stop_button_a', 'emergency_stop_button_b', 'circuit_breaker', 'circular_dial_small_b', 'circular_dial_small_c', 'circular_dial_small_d', 'circular_dial_c', 'circular_dial_d', 'circular_dial_e', 'circular_dial_f', 'circular_dial_g', 'circular_dial_h', 'alternator_motor', 'hinge_pin', 'control_fin_a', 'control_fin_b', 'control_fin_c', 'tyre_mount', 'latch_handle', 'rail_ballscrew', 'hydraulic_actuator', 'actuator_stepper_motor', 'latch_pin', 'latch_knuckle', 'hydraulic_pump', 'pitot_tube', 'electric_motor_a', 'electric_motor_b', 'electric_motor_c', 'smoke_discharger', 'catalytic', 'angle_bracket', 'handbrake', 'landing_gear_dual', 'drive_shaft_b', 'ladder', 'gear_stick', 'rail', 'rail_slider', 'air_filter', 'flight_yoke', 'flight_stick_jet', 'flight_stick', 'rail_ballscrew_slider', 'liquid_pump', 'hinge_knuckle', 'mounting_pin', 'mounting_knuckle', 'differential_gearbox_b', 'pulley_wheel', 'liquid_port_straight', 'liquid_port_angle', 'gas_port_2_straight', 'gas_port_2_angle', 'liquid_port_2_straight', 'liquid_port_2_angle', 'mechanical_interface_out_straight', 'electrical_interface_straight', 'gas_port_straight', 'gas_pump', 'exhaust_manifold_angle', 'air_manifold', 'air_manifold_2', 'exhaust_manifold_straight', 'fuel_manifold', 'oil_manifold', 'coolant_manifold', 'battery_b', 'electric_port_straight', 'electric_port_angle', 'torque_interface_straight', 'gas_interface_straight', 'liquid_interface_straight', 'mechanical_bracket', 'electric_bracket', 'electric_junction', 'junction_x_liquid_pipe_a', 'junction_t_liquid_pipe_a', 'junction_x_gas_pipe_a', 'junction_t_gas_pipe_a', 'mechanical_junction', 'mechanical_junction_abs', 'mechanical_junction_invert', 'mechanical_junction_max', 'mechanical_junction_min', 'mechanical_junction_offset', 'mechanical_junction_scale', 'mechanical_junctions_set_reset', 'mechanical_junction_toggle', 'electric_relay', 'square_bracket', 'mechanical_junction_add', 'gas_vent', 'liquid_vent', 'liquid_bracket', 'gas_bracket', 'data_bracket', 'gas_tank_a', 'gas_tank_b', 'gas_tank_c', 'wheel_b', 'drive_shaft_c', 'mechanical_interface_in_straight', 'turbo_b', 'electrical_interface_angle', 'gas_interface_angle', 'liquid_interface_angle', 'torque_interface_angle', 'mechanical_interface_in_angle', 'mechanical_interface_out_angle', 'tyre_mount_b', 'roller_wheel_fixed_a', 'roller_wheel_fixed_b', 'roller_wheel_fixed_c', 'roller_wheel_fixed_d', 'roller_wheel_fixed_e', 'roller_wheel_fixed_f', 'sprocket_a', 'sprocket_b', 'sprocket_c', 'sprocket_d', 'sprocket_e', 'sprocket_f', 'jet_engine_a', 'jet_compressor_a', 'jet_accessory_gearbox_a', 'jet_particle_separator_a', 'jet_exhaust_a', 'roller_wheel_suspension_a', 'roller_wheel_suspension_b', 'roller_wheel_suspension_c', 'roller_wheel_suspension_d', 'roller_wheel_suspension_e', 'roller_wheel_suspension_f', 'gas_port_angle', 'autocannon_40mm', 'cannon_120mm', 'liquid_fill_port', 'building_floor_sq', 'building_floor_angle', 'building_floor_corner', 'building_floor_straight', 'building_wall_angle', 'building_wall_base_angle', 'building_wall_base_cross', 'building_wall_base_end', 'building_wall_base_straight', 'building_wall_base_t', 'building_wall_cross', 'building_wall_end', 'building_wall_straight', 'building_wall_t', 'building_wall_top_angle', 'building_wall_top_cross', 'building_wall_top_end', 'building_wall_top_straight', 'building_wall_top_t', 'building_outer_frame_a', 'building_outer_straight', 'building_outer_concave', 'building_outer_convex', 'building_outer_frame_lower_a', 'building_outer_frame_lower_b', 'building_outer_frame_upper_a', 'building_outer_frame_upper_b', 'building_stair_base_a', 'building_stair_base_b', 'building_stair_base_c', 'building_stair_land_a', 'building_stair_land_b', 'building_stair_land_c', 'building_stair_riser_a', 'building_stair_riser_b', 'building_stair_riser_c', 'building_roof_pitch', 'building_roof_pitch_cap_a', 'building_roof_pitch_cap_b', 'building_roof_pitch_end_a', 'building_roof_pitch_end_b', 'building_roof_pitch_fold_concave', 'building_roof_pitch_fold_convex', 'building_roof_pitch_wall', 'building_roof_pitch_wall_cap_a', 'building_roof_pitch_wall_cap_b', 'building_floor_infill_a', 'building_floor_infill_b', 'building_door', 'building_window', 'building_wall_frame_lower', 'building_wall_frame_upper', 'building_outer_frame_b', 'building_outer_frame_lower_c', 'building_outer_frame_upper_c', 'building_wall_frame', 'building_wall_base_frame', 'building_outer_frame_base_lower_a', 'building_outer_frame_base_lower_b', 'building_door_interior', 'microcontroller', 'data_port_straight', 'data_port_angle', 'data_junction', 'data_interface_straight', 'data_interface_angle', 'entity_interface', 'jet_engine_fuel_manifold', 'liquid_pressure_sensor', 'gas_pressure_sensor', 'liquid_temperature_sensor', 'gas_temperature_sensor', 'liquid_valve_straight', 'liquid_valve_t', 'gas_valve_straight', 'gas_valve_t', 'mechanical_handle', 'heat_exchanger_liquid_liquid', 'heat_exchanger_gas_gas', 'heat_exchanger_gas_liquid', 'rotor_heli_a', 'weapon_mount', 'jet_nosecone_gearbox', 'rotor_heli_b', 'brake', 'clutch', 'gearbox_fixed_ratio', 'microphone', 'hydraulic_cylinder_connector_base', 'hydraulic_cylinder_connector', 'v_engine_b', 'v_engine_c', 'opposed_engine_b', 'opposed_engine_c', 'weight_block', 'engine_wheel_b', 'engine_wheel_c', 'air_filter_b', 'short_shifter', 'radiator_fan_a', 'radiator_fan_b', 'radiator_fan_c', 'radiator_fan_d', 'radiator_b', 'wheel_c', 'exhaust_manifold_angle_b', 'exhaust_manifold_straight_b', 'gas_vent_b', 'fuel_manifold_b', 'oil_manifold_b', 'coolant_manifold_b', 'junction_x_liquid_pipe_b', 'junction_x_gas_pipe_b', 'junction_t_liquid_pipe_b', 'junction_t_gas_pipe_b', 'liquid_bracket_b', 'gas_bracket_b', 'liquid_valve_straight_b', 'gas_valve_straight_b', 'gas_straight_reducer_a_b', 'liquid_straight_reducer_a_b', 'boat_rudder_a', 'boat_rudder_b', 'boat_rudder_c', 'boat_propeller_a', 'boat_propeller_b', 'boat_propeller_c', 'keycard_reader', 'hydraulic_cylinder_connector_base_2_2', 'hydraulic_cylinder_connector_2_2', 'hydraulic_cylinder_connector_base_3_3', 'hydraulic_cylinder_connector_3_3', 'lever_switch_curve_a', 'fusebox', 'lever_switch_a', 'lever_switch_b', 'turbo_c', 'turbo_d', 'pulley_a', 'pulley_straight_a', 'pulley_corner_a', 'acceleration_sensor', 'tilt_sensor', 'compass_sensor', 'gyro_rotation_sensor']

FULL_COMP_BUILDING = ['chair_a', 'chair_b', 'deckchair_a', 'stool_a', 'toilet_a', 'sink_a', 'bath_a', 'pouffe_a', 'pouffe_b', 'sofa_a', 'armchair_a', 'sofa_b', 'sofa_c', 'wardrobe_a', 'wardrobe_b', 'side_table_a', 'side_table_b', 'side_table_c', 'tv_a', 'tv_b', 'table_a', 'table_b', 'lamp_a', 'lamp_b', 'book_shelf_a', 'book_shelf_b', 'desk_a', 'coffee_table_a', 'record_cube_a', 'bed_a', 'bed_b', 'king_bed_a', 'king_bed_b', 'washer_a', 'dryer_a', 'fridge_a', 'cooker_a', 'filing_cabinet_a', 'paper_bin_a', 'trashcan_b', 'work_cubical_b', 'work_cubical_a', 'work_desk_a', 'police_desk_a', 'interrogation_desk_a', 'vending_machine_a', 'letter_sorter_a', 'office_cabinet_a', 'watercooler_a', 'filing_cabinet_b', 'chair_d', 'fan_a', 'printer_a', 'break_room_table_a', 'cleaning_dolly_a', 'wet_floor_sign_a', 'desk_chair_a', 'desk_chair_b', 'chair_c', 'whiteboard_a', 'line_barricade_a', 'barricade_a', 'hose_reel_a', 'hose_pump_a', 'cone_a', 'office_cabinet_b', 'locker_a', 'locker_b', 'locker_c', 'bench_a', 'bench_b', 'store_shelves_a', 'store_shelves_b', 'store_shelves_c', 'till_a', 'trolly_a', 'drinks_cooler_a', 'store_freezer_a', 'convenience_till_a', 'doctors_bed_a', 'autopsy_table_a', 'autopsy_sink_a', 'surgical_trolly_a', 'paper_bin_b', 'doctor_desk_a', 'hospital_bed_a', 'hospital_bed_b', 'hospital_divider_a', 'hospital_divider_b', 'waiting_seats_a', 'nurses_trolly_a', 'sainitizer_a', 'anesthesia_machine_a', 'medical_waste_a', 'baby_bed_a', 'baby_incubator_a', 'defibrillator_b', 'defibrillator_a', 'heart_monitor_a', 'iv_drip_a', 'ecg_a', 'medical_gas_tank_b', 'medical_gas_tank_a', 'blood_pressure_a', 'wheelchair_a', 'surgical_light_a', 'shelving_a', 'shelving_b', 'shelving_c', 'lumber_shelving_b', 'lumber_shelving_a', 'shelving_d', 'storage_box_f', 'storage_box_e', 'pallet_a', 'pallet_b', 'storage_box_g', 'storage_box_b', 'storage_box_a', 'storage_box_d', 'storage_box_c', 'tool_cabinet_a', 'barrel_b', 'barrel_a', 'storage_holder_a', 'wearhouse_dolly_a', 'barrier_a', 'storage_sack_a', 'hangar_dolly_a', 'chainsaw_jig', 'saw_setup_a', 'water_tank_a', 'pallet_jack_a', 'fuel_tank_a', 'hand_trucks_a', 'hangar_fan_a', 'doctor_cabinet_a', 'workshop_cabinet_a', 'log_deck_a', 'log_conveyor_a', 'wooden_planks_a', 'covered_planks_a', 'posts_a', 'covered_planks_b', 'saw_a', 'ladder_a', 'bar_a', 'pool_table_a', 'jukebox_a', 'restaurant_table_d', 'chair_f', 'chair_g', 'stool_d', 'restaurant_table_c', 'restaurant_table_e', 'restaurant_table_b', 'restaurant_table_a', 'stool_c', 'diner_chair_a', 'diner_table_b', 'booth_c', 'booth_b', 'booth_a', 'diner_table_a', 'restaurant_fridge_a', 'fryer_a', 'cooking_storage_a', 'restaurant_grill_a', 'restaurant_oven_a', 'restaurant_range_a', 'restaurant_range_b', 'tray_return_a', 'restaurant_trolly_a', 'restaurant_sink_a', 'restaurant_bin_a', 'hotel_bed_set_a', 'hotel_bed_a', 'hotel_chair_a', 'hotel_coffetable_a', 'hotel_coffetable_b', 'hotel_desk_a', 'hotel_side_tv_a', 'ice_machine_a', 'hotel_counter_a', 'laundry_trolley_a', 'minifridge_a', 'hotel_cleaning_dolly_a', 'luggage_trolley_a', 'hotel_dresser_a', 'hotel_bed_pouffe_a', 'hotel_storage_grid_a', 'bleachers_a', 'basketball_net_a', 'science_lab_cabinet_a', 'school_coat_hooks_a', 'tv_av_set_a', 'school_draws_a', 'cubed_shelves_b', 'school_computer_a', 'book_shelf_c', 'teachers_desk_a', 'stool_b', 'vaulting_buck_a', 'book_shelf_d', 'vaulting_buck_b', 'science_lab_table_a', 'chalkboard_a', 'projector_a', 'trashcan_a', 'school_chair_a', 'school_desk_a', 'church_organ_a', 'church_chair_a', 'chair_e', 'confessional_a', 'church_pew_a', 'church_alter_a', 'church_desk_a', 'church_alter_b', 'church_basin_a', 'hotel_bedside_a', 'vehicle_container', 'cooler_unit_a', 'ac_unit_a', 'portable_sign_a', 'gas_pump_a', 'rooftop_satellite_a', 'door_lamp_a', 'tap_a', 'hose_a', 'sign_shop_a', 'sign_shop_b', 'sign_shop_c', 'lab_table_a', 'lab_table_b', 'lab_table_c', 'lab_robot_arm_a', 'lab_standing_autoclave_a', 'lab_centrifuge_a', 'lab_automated_analyser_a', 'lab_chemistry_diagnostics_machine_a', 'lab_fridge_a', 'lab_fridge_b', 'metal_bandsaw_a', 'metal_lathe_a', 'metal_milling_machine_a', 'workshop_desk_a', 'workshop_desk_b']


ALPHA = 'abcdefghijklmnopqrstuvwxyz234567'
NUM_PAINTS = 256
PAINT_SLOT = 25

def b32_lsb_encode(data):
    out = []; acc = nb = 0
    for byte in data:
        acc |= byte << nb; nb += 8
        while nb >= 5:
            out.append(ALPHA[acc & 0x1f]); acc >>= 5; nb -= 5
    if nb > 0: out.append(ALPHA[acc & 0x1f])
    return ''.join(out)

def b32_lsb_decode(text):
    rev = [c for c in ALPHA]; ri = [c for c in ALPHA]
    revmap = dict((c, i) for i, c in enumerate(ALPHA))
    out = bytearray(); acc = nb = 0
    for ch in text.strip().lower():
        if ch not in revmap: continue
        acc |= revmap[ch] << nb; nb += 5
        while nb >= 8:
            out.append(acc & 0xff); acc >>= 8; nb -= 8
    return bytes(out)

def xor(data, key):
    return bytes(data[i] ^ key[i % len(key)] for i in range(len(data)))

def save_dir():
    ad = os.environ.get('APPDATA', '')
    d = os.path.join(ad, 'Anymaker')
    return d if os.path.isdir(d) else ''

def unlocks_path(d): return os.path.join(d, 'unlocks.txt')
def backup_path(d):  return os.path.join(d, 'unlocks.txt.backup')

def detect_steam_id(d):
    for p in (unlocks_path(d), backup_path(d)):
        if os.path.isfile(p):
            try:
                enc = b32_lsb_decode(open(p, encoding='utf-8', errors='ignore').read())
                prefix = b'{\n    "unlocked_items"'
                key = bytes(enc[i] ^ prefix[i] for i in range(min(len(prefix), len(enc))))[:17]
                if len(key) == 17 and key.isdigit() and key.startswith(b'7656'):
                    return key.decode()
            except Exception:
                pass
    return ''

def build_unlock_text(steam_id, full=False):
    if full:
        item_ids = FULL_ITEMS; cr = FULL_COMP_REGULAR; cb = FULL_COMP_BUILDING
    else:
        item_ids = SAFE_ITEMS; cr = SAFE_COMP_REGULAR; cb = SAFE_COMP_BUILDING
    items = [{"definition_id": d} for d in item_ids]
    items += [{"definition_id": "vehicle_editor_add_component", "component_definition_id": c} for c in cr]
    items += [{"definition_id": "vehicle_editor_add_building_component", "component_definition_id": c} for c in cb]
    items += [{"definition_id": "vehicle_editor_paint", "pattern_index": PAINT_SLOT, "paint_index": p} for p in range(NUM_PAINTS)]
    seen = set(); uniq = []
    for it in items:
        k = json.dumps(it, sort_keys=True)
        if k not in seen:
            seen.add(k); uniq.append(it)
    text = json.dumps({"unlocked_items": uniq}, indent=4, ensure_ascii=False)
    return b32_lsb_encode(xor(text.encode('utf-8'), steam_id.encode())), len(uniq)

def do_patch(d, steam_id, full, log):
    up = unlocks_path(d); bp = backup_path(d)
    if not (len(steam_id) == 17 and steam_id.isdigit()):
        raise ValueError("Нужен корректный SteamID64 (17 цифр).")
    if os.path.isfile(up) and not os.path.isfile(bp):
        shutil.copy2(up, bp); log("Создан бэкап оригинала: unlocks.txt.backup")
    out, n = build_unlock_text(steam_id, full)
    open(up, 'w', encoding='utf-8').write(out)
    mode = "ПОЛНЫЙ (tier 3+!)" if full else "безопасный"
    log("Записано {} разблокировок [{}], ~{} КБ.".format(n, mode, len(out)//1024))
    if full:
        log("ВНИМАНИЕ: это включает пасхалку — рыба + блокировка сохранения. Только для изучения.")
    log("Закройте игру и Steam, затем запустите заново.")

def do_rollback(d, log):
    up = unlocks_path(d); bp = backup_path(d)
    if not os.path.isfile(bp):
        raise FileNotFoundError("Бэкап unlocks.txt.backup не найден — откатывать не к чему.")
    shutil.copy2(bp, up)
    log("Откат выполнен: восстановлен исходный unlocks.txt.")
    log("Закройте игру и Steam, затем запустите заново.")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Anymaker Unlock")
        self.geometry("600x470"); self.resizable(False, False)
        self.dir = save_dir()
        self.sid = tk.StringVar(value=detect_steam_id(self.dir) if self.dir else '')
        self.full = tk.BooleanVar(value=False)

        ttk.Label(self, text="Anymaker Unlock", font=('Segoe UI', 15, 'bold')).pack(pady=8)

        frm = ttk.Frame(self); frm.pack(fill='x', padx=12)
        ttk.Label(frm, text="Папка сейвов:").grid(row=0, column=0, sticky='w')
        self.dir_var = tk.StringVar(value=self.dir or '(не найдена)')
        ttk.Entry(frm, textvariable=self.dir_var, width=50).grid(row=0, column=1, sticky='w')
        ttk.Button(frm, text="...", width=3, command=self.pick_dir).grid(row=0, column=2, padx=4)
        ttk.Label(frm, text="SteamID64:").grid(row=1, column=0, sticky='w', pady=4)
        ttk.Entry(frm, textvariable=self.sid, width=50).grid(row=1, column=1, sticky='w', pady=4)

        chk = ttk.Checkbutton(self, variable=self.full,
            text="Полный анлок: открыть ВСЁ, включая tier 3+ (для изучения)")
        chk.pack(anchor='w', padx=14, pady=(6, 0))
        ttk.Label(self, foreground='#b00',
            text="⚠ Полный режим включает пасхалку: рыба вокруг головы + блокировка сохранения мира.",
            wraplength=560, justify='left').pack(anchor='w', padx=30)

        btns = ttk.Frame(self); btns.pack(pady=8)
        ttk.Button(btns, text="Пропатчить (разблокировать)", width=32, command=self.on_patch).grid(row=0, column=0, padx=6, pady=4)
        ttk.Button(btns, text="Откатить к оригиналу", width=32, command=self.on_rollback).grid(row=1, column=0, padx=6, pady=4)

        ttk.Label(self, text="Лог:").pack(anchor='w', padx=12)
        self.txt = tk.Text(self, height=8, width=70, state='disabled', wrap='word')
        self.txt.pack(padx=12, pady=4)

        if not self.dir:
            self.log("Не нашёл %APPDATA%\\Anymaker — укажите папку кнопкой «...».")
        elif not self.sid.get():
            self.log("Не удалось определить SteamID — впишите вручную (17 цифр).")
        else:
            self.log("Папка и SteamID определены: " + self.sid.get())

    def pick_dir(self):
        p = filedialog.askdirectory(title="Папка Anymaker (с unlocks.txt)")
        if p:
            self.dir = p; self.dir_var.set(p)
            if not self.sid.get(): self.sid.set(detect_steam_id(p))

    def log(self, msg):
        self.txt.configure(state='normal'); self.txt.insert('end', msg + "\n")
        self.txt.see('end'); self.txt.configure(state='disabled')

    def _check(self):
        if not self.dir or not os.path.isdir(self.dir):
            messagebox.showerror("Ошибка", "Укажите папку сейвов Anymaker."); return False
        return True

    def on_patch(self):
        if not self._check(): return
        full = self.full.get()
        if full and not messagebox.askyesno("Полный анлок",
            "Полный режим откроет контент полной игры (tier 3+) и ВКЛЮЧИТ пасхалку:\n"
            "рыба вокруг головы и блокировка сохранения мира.\n\nПродолжить?"):
            return
        try:
            do_patch(self.dir, self.sid.get().strip(), full, self.log)
            messagebox.showinfo("Готово", "Применено. Перезапустите игру.")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e)); self.log("Ошибка: " + str(e))

    def on_rollback(self):
        if not self._check(): return
        try:
            do_rollback(self.dir, self.log)
            messagebox.showinfo("Готово", "Откат выполнен. Перезапустите игру.")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e)); self.log("Ошибка: " + str(e))

if __name__ == "__main__":
    App().mainloop()
