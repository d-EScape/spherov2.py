from collections import OrderedDict
from enum import IntEnum
from functools import lru_cache, partialmethod

from spherov2.commands.animatronic import Animatronic
from spherov2.commands.api_and_shell import ApiAndShell
from spherov2.commands.connection import Connection
from spherov2.commands.drive import Drive
from spherov2.commands.factory_test import FactoryTest
from spherov2.commands.firmware import Firmware
from spherov2.commands.io import IO
from spherov2.commands.power import Power
from spherov2.commands.sensor import Sensor
from spherov2.commands.system_info import SystemInfo
from spherov2.controls.v2 import DriveControl, LedControl, SensorControl
from spherov2.toy import ToySensor, Toy, ToyV2
from spherov2.types import ToyType


class R2D2(ToyV2):
    toy_type = ToyType('R2-D2', 'D2-', 'D2', .12)
    _handshake = [('00020005-574f-4f20-5370-6865726f2121', bytearray(b'usetheforce...band'))]

    class LEDs(IntEnum):
        FRONT_RED = 0
        FRONT_GREEN = 1
        FRONT_BLUE = 2
        LOGIC_DISPLAYS = 3
        BACK_RED = 4
        BACK_GREEN = 5
        BACK_BLUE = 6
        HOLO_PROJECTOR = 7

    class Audio(IntEnum):
        TEST_1497HZ = 1
        TEST_200HZ = 32
        TEST_2517HZ = 63
        TEST_3581HZ = 94
        TEST_431HZ = 125
        TEST_6011HZ = 156
        TEST_853HZ = 187
        BB8_ALARM_1 = 218
        BB8_ALARM_10 = 235
        BB8_ALARM_11 = 254
        BB8_ALARM_12 = 258
        BB8_ALARM_2 = 264
        BB8_ALARM_3 = 268
        BB8_ALARM_4 = 272
        BB8_ALARM_6 = 279
        BB8_ALARM_7 = 288
        BB8_ALARM_8 = 296
        BB8_ALARM_9 = 301
        BB8_BOOT_UP = 309
        BB8_BOOR_UP_2 = 330
        BB8_CHATTY_1 = 352
        BB8_CHATTY_10 = 356
        BB8_CHATTY_11 = 360
        BB8_CHATTY_12 = 368
        BB8_CHATTY_13 = 375
        BB8_CHATTY_14 = 381
        BB8_CHATTY_15 = 390
        BB8_CHATTY_16 = 397
        BB8_CHATTY_17 = 404
        BB8_CHATTY_18 = 410
        BB8_CHATTY_19 = 417
        BB8_CHATTY_2 = 430
        BB8_CHATTY_20 = 464
        BB8_CHATTY_22 = 471
        BB8_CHATTY_23 = 479
        BB8_CHATTY_24 = 492
        BB8_CHATTY_25 = 518
        BB8_CHATTY_26 = 525
        BB8_CHATTY_27 = 537
        BB8_CHATTY_3 = 544
        BB8_CHATTY_4 = 557
        BB8_CHATTY_5 = 570
        BB8_CHATTY_6 = 577
        BB8_CHATTY_7 = 581
        BB8_CHATTY_8 = 587
        BB8_CHATTY_9 = 599
        BB8_DONT_KNOW = 606
        BB8_EXCITED_1 = 612
        BB8_EXCITED_2 = 622
        BB8_EXCITED_3 = 630
        BB8_EXCITED_4 = 644
        BB8_HEY_1 = 671
        BB8_HEY_10 = 682
        BB8_HEY_11 = 686
        BB8_HEY_12 = 690
        BB8_HEY_13 = 700
        BB8_HEY_2 = 724
        BB8_HEY_3 = 732
        BB8_HEY_4 = 734
        BB8_HEY_5 = 739
        BB8_HEY_6 = 743
        BB8_HEY_7 = 747
        BB8_HEY_8 = 753
        BB8_HEY_9 = 757
        BB8_LAUGH_1 = 761
        BB8_LAUGH_2 = 764
        BB8_NEGATIVE_1 = 787
        BB8_NEGATIVE_10 = 792
        BB8_NEGATIVE_11 = 802
        BB8_NEGATIVE_12 = 813
        BB8_NEGATIVE_13 = 825
        BB8_NEGATIVE_14 = 831
        BB8_NEGATIVE_15 = 836
        BB8_NEGATIVE_16 = 859
        BB8_NEGATIVE_17 = 867
        BB8_NEGATIVE_18 = 874
        BB8_NEGATIVE_19 = 888
        BB8_NEGATIVE_2 = 896
        BB8_NEGATIVE_20 = 902
        BB8_NEGATIVE_21 = 916
        BB8_NEGATIVE_22 = 927
        BB8_NEGATIVE_23 = 935
        BB8_NEGATIVE_24 = 946
        BB8_NEGATIVE_25 = 953
        BB8_NEGATIVE_26 = 963
        BB8_NEGATIVE_27 = 969
        BB8_NEGATIVE_28 = 983
        BB8_NEGATIVE_29 = 988
        BB8_NEGATIVE_3 = 998
        BB8_NEGATIVE_30 = 1003
        BB8_NEGATIVE_4 = 1010
        BB8_NEGATIVE_5 = 1020
        BB8_NEGATIVE_6 = 1032
        BB8_NEGATIVE_7 = 1040
        BB8_NEGATIVE_8 = 1052
        BB8_NEGATIVE_9 = 1064
        BB8_POSITIVE_1 = 1077
        BB8_POSITIVE_10 = 1082
        BB8_POSITIVE_11 = 1087
        BB8_POSITIVE_12 = 1092
        BB8_POSITIVE_13 = 1096
        BB8_POSITIVE_14 = 1102
        BB8_POSITIVE_15 = 1109
        BB8_POSITIVE_16 = 1113
        BB8_POSITIVE_2 = 1118
        BB8_POSITIVE_3 = 1123
        BB8_POSITIVE_4 = 1130
        BB8_POSITIVE_5 = 1135
        BB8_POSITIVE_6 = 1138
        BB8_POSITIVE_7 = 1147
        BB8_POSITIVE_8 = 1150
        BB8_POSITIVE_9 = 1157
        BB8_SAD_1 = 1163
        BB8_SAD_10 = 1170
        BB8_SAD_11 = 1178
        BB8_SAD_12 = 1186
        BB8_SAD_13 = 1192
        BB8_SAD_14 = 1199
        BB8_SAD_15 = 1205
        BB8_SAD_16 = 1213
        BB8_SAD_17 = 1220
        BB8_SAD_18 = 1230
        BB8_SAD_2 = 1236
        BB8_SAD_3 = 1240
        BB8_SAD_4 = 1250
        BB8_SAD_5 = 1268
        BB8_SAD_6 = 1275
        BB8_SAD_7 = 1281
        BB8_SAD_8 = 1295
        BB8_SAD_9 = 1303
        BB8_SHORTCUT = 1308
        BB8_WOW_1 = 1324
        BB9E_ALARM_1 = 1329
        BB9E_ALARM_2 = 1347
        BB9E_ALARM_3 = 1363
        BB9E_ALARM_4 = 1375
        BB9E_ALARM_5 = 1384
        BB9E_CHATTY_1 = 1394
        BB9E_CHATTY_2 = 1408
        BB9E_EXCITED_1 = 1432
        BB9E_EXCITED_2 = 1442
        BB9E_EXCITED_3 = 1463
        BB9E_HEY_1 = 1476
        BB9E_HEY_2 = 1486
        BB9E_NEGATIVE_1 = 1494
        BB9E_NEGATIVE_2 = 1505
        BB9E_NEGATIVE_3 = 1516
        BB9E_NEGATIVE_4 = 1523
        BB9E_POSITIVE_1 = 1531
        BB9E_POSITIVE_2 = 1549
        BB9E_POSITIVE_3 = 1558
        BB9E_POSITIVE_4 = 1571
        BB9E_POSITIVE_5 = 1583
        BB9E_SAD_1 = 1592
        BB9E_SAD_2 = 1600
        R2_FALL = 1609
        R2_HIT_1 = 1623
        R2_HIT_10 = 1628
        R2_HIT_11 = 1635
        R2_HIT_2 = 1642
        R2_HIT_3 = 1647
        R2_HIT_4 = 1653
        R2_HIT_5 = 1659
        R2_HIT_6 = 1664
        R2_HIT_7 = 1669
        R2_HIT_8 = 1676
        R2_HIT_9 = 1684
        R2_STEP_1 = 1690
        R2_STEP_2 = 1693
        R2_STEP_3 = 1696
        R2_STEP_4 = 1698
        R2_STEP_5 = 1700
        R2_STEP_6 = 1702
        R2_ACCESS_PANELS = 1704
        R2_ALARM_1 = 1737
        R2_ALARM_10 = 1747
        R2_ALARM_12 = 1756
        R2_ALARM_13 = 1763
        R2_ALARM_14 = 1771
        R2_ALARM_15 = 1784
        R2_ALARM_16 = 1791
        R2_ALARM_2 = 1809
        R2_ALARM_3 = 1821
        R2_ALARM_4 = 1831
        R2_ALARM_5 = 1835
        R2_ALARM_6 = 1843
        R2_ALARM_7 = 1858
        R2_ALARM_8 = 1867
        R2_ALARM_9 = 1893
        R2_ANNOYED = 1910
        R2_BURNOUT = 1915
        R2_CHATTY_1 = 1950
        R2_CHATTY_10 = 1959
        R2_CHATTY_11 = 1966
        R2_CHATTY_12 = 1977
        R2_CHATTY_13 = 1987
        R2_CHATTY_14 = 2002
        R2_CHATTY_15 = 2007
        R2_CHATTY_16 = 2010
        R2_CHATTY_17 = 2019
        R2_CHATTY_18 = 2028
        R2_CHATTY_19 = 2039
        R2_CHATTY_2 = 2061
        R2_CHATTY_20 = 2072
        R2_CHATTY_21 = 2080
        R2_CHATTY_22 = 2085
        R2_CHATTY_23 = 2095
        R2_CHATTY_24 = 2105
        R2_CHATTY_25 = 2121
        R2_CHATTY_26 = 2132
        R2_CHATTY_27 = 2143
        R2_CHATTY_28 = 2157
        R2_CHATTY_29 = 2170
        R2_CHATTY_3 = 2174
        R2_CHATTY_30 = 2184
        R2_CHATTY_31 = 2188
        R2_CHATTY_32 = 2198
        R2_CHATTY_33 = 2202
        R2_CHATTY_34 = 2211
        R2_CHATTY_35 = 2221
        R2_CHATTY_36 = 2232
        R2_CHATTY_37 = 2241
        R2_CHATTY_38 = 2253
        R2_CHATTY_39 = 2264
        R2_CHATTY_4 = 2276
        R2_CHATTY_40 = 2285
        R2_CHATTY_41 = 2292
        R2_CHATTY_42 = 2307
        R2_CHATTY_43 = 2322
        R2_CHATTY_44 = 2332
        R2_CHATTY_45 = 2344
        R2_CHATTY_46 = 2357
        R2_CHATTY_47 = 2368
        R2_CHATTY_48 = 2377
        R2_CHATTY_49 = 2387
        R2_CHATTY_5 = 2399
        R2_CHATTY_50 = 2413
        R2_CHATTY_51 = 2424
        R2_CHATTY_52 = 2439
        R2_CHATTY_53 = 2452
        R2_CHATTY_54 = 2457
        R2_CHATTY_55 = 2463
        R2_CHATTY_56 = 2474
        R2_CHATTY_57 = 2492
        R2_CHATTY_58 = 2509
        R2_CHATTY_59 = 2519
        R2_CHATTY_6 = 2524
        R2_CHATTY_60 = 2535
        R2_CHATTY_61 = 2543
        R2_CHATTY_62 = 2554
        R2_CHATTY_7 = 2562
        R2_CHATTY_8 = 2572
        R2_CHATTY_9 = 2579
        R2_ENGAGE_HYPER_DRIVE = 2586
        R2_EXCITED_1 = 2600
        R2_EXCITED_10 = 2615
        R2_EXCITED_11 = 2633
        R2_EXCITED_12 = 2644
        R2_EXCITED_13 = 2654
        R2_EXCITED_14 = 2662
        R2_EXCITED_15 = 2680
        R2_EXCITED_16 = 2691
        R2_EXCITED_2 = 2708
        R2_EXCITED_3 = 2726
        R2_EXCITED_4 = 2730
        R2_EXCITED_5 = 2736
        R2_EXCITED_6 = 2753
        R2_EXCITED_7 = 2767
        R2_EXCITED_8 = 2777
        R2_EXCITED_9 = 2787
        R2_HEAD_SPIN = 2797
        R2_HEY_1 = 2813
        R2_HEY_10 = 2824
        R2_HEY_11 = 2828
        R2_HEY_12 = 2833
        R2_HEY_2 = 2841
        R2_HEY_3 = 2856
        R2_HEY_4 = 2861
        R2_HEY_5 = 2882
        R2_HEY_6 = 2893
        R2_HEY_7 = 2898
        R2_HEY_8 = 2904
        R2_HEY_9 = 2912
        R2_LAUGH_1 = 2919
        R2_LAUGH_2 = 2935
        R2_LAUGH_3 = 2950
        R2_LAUGH_4 = 2955
        R2_MOTOR = 2970
        R2_NEGATIVE_1 = 3101
        R2_NEGATIVE_10 = 3111
        R2_NEGATIVE_11 = 3115
        R2_NEGATIVE_12 = 3121
        R2_NEGATIVE_13 = 3132
        R2_NEGATIVE_14 = 3136
        R2_NEGATIVE_15 = 3148
        R2_NEGATIVE_16 = 3152
        R2_NEGATIVE_17 = 3157
        R2_NEGATIVE_18 = 3164
        R2_NEGATIVE_19 = 3167
        R2_NEGATIVE_2 = 3172
        R2_NEGATIVE_20 = 3178
        R2_NEGATIVE_21 = 3191
        R2_NEGATIVE_22 = 3200
        R2_NEGATIVE_23 = 3213
        R2_NEGATIVE_24 = 3219
        R2_NEGATIVE_25 = 3226
        R2_NEGATIVE_26 = 3230
        R2_NEGATIVE_27 = 3233
        R2_NEGATIVE_28 = 3241
        R2_NEGATIVE_3 = 3251
        R2_NEGATIVE_4 = 3258
        R2_NEGATIVE_5 = 3263
        R2_NEGATIVE_6 = 3268
        R2_NEGATIVE_7 = 3274
        R2_NEGATIVE_8 = 3282
        R2_NEGATIVE_9 = 3291
        R2_POSITIVE_1 = 3302
        R2_POSITIVE_10 = 3309
        R2_POSITIVE_11 = 3318
        R2_POSITIVE_12 = 3326
        R2_POSITIVE_13 = 3340
        R2_POSITIVE_14 = 3353
        R2_POSITIVE_15 = 3358
        R2_POSITIVE_16 = 3364
        R2_POSITIVE_17 = 3369
        R2_POSITIVE_18 = 3375
        R2_POSITIVE_19 = 3388
        R2_POSITIVE_2 = 3394
        R2_POSITIVE_20 = 3403
        R2_POSITIVE_21 = 3410
        R2_POSITIVE_22 = 3422
        R2_POSITIVE_23 = 3434
        R2_POSITIVE_3 = 3439
        R2_POSITIVE_4 = 3446
        R2_POSITIVE_5 = 3449
        R2_POSITIVE_6 = 3454
        R2_POSITIVE_7 = 3460
        R2_POSITIVE_8 = 3471
        R2_POSITIVE_9 = 3478
        R2_SAD_1 = 3484
        R2_SAD_10 = 3495
        R2_SAD_11 = 3518
        R2_SAD_12 = 3526
        R2_SAD_13 = 3536
        R2_SAD_14 = 3543
        R2_SAD_15 = 3553
        R2_SAD_16 = 3561
        R2_SAD_17 = 3570
        R2_SAD_18 = 3593
        R2_SAD_19 = 3600
        R2_SAD_2 = 3608
        R2_SAD_20 = 3612
        R2_SAD_21 = 3619
        R2_SAD_22 = 3632
        R2_SAD_23 = 3639
        R2_SAD_24 = 3649
        R2_SAD_25 = 3661
        R2_SAD_3 = 3686
        R2_SAD_4 = 3693
        R2_SAD_5 = 3703
        R2_SAD_6 = 3739
        R2_SAD_7 = 3755
        R2_SAD_8 = 3782
        R2_SAD_9 = 3790
        R2_SCREAM = 3797
        R2_SCREAM_2 = 3810
        R2_SHORT_OUT = 3825
        R2Q5_ALARM_1 = 3864
        R2Q5_ALARM_2 = 3869
        R2Q5_CHATTY_1 = 3875
        R2Q5_CHATTY_2 = 3891
        R2Q5_HEY_1 = 3896
        R2Q5_HEY_2 = 3901
        R2Q5_NEGATIVE_1 = 3907
        R2Q5_POSITIVE_1 = 3914
        R2Q5_POSITIVE_2 = 3920
        R2Q5_SAD_1 = 3925
        R2Q5_SHUTDOWN = 3929
        BB9E_EXTRA_1 = 3941
        BB9E_EXTRA_2 = 4021
        BB9E_EXTRA_3 = 4246
        BB9E_EXTRA_4 = 4568
        BB9E_EXTRA_5 = 4929
        BB9E_EXTRA_6 = 5156
        BB9E_EXTRA_7 = 5315
        BB9E_HEAD_TURN_1 = 5441
        BB9E_HEAD_TURN_2 = 5483
        BB9E_HEAD_TURN_3 = 5513

    class Animations(IntEnum):
        CHARGER_1 = 0
        CHARGER_2 = 1
        CHARGER_3 = 2
        CHARGER_4 = 3
        CHARGER_5 = 4
        CHARGER_6 = 5
        CHARGER_7 = 6
        EMOTE_ALARM = 7
        EMOTE_ANGRY = 8
        EMOTE_ATTENTION = 9
        EMOTE_FRUSTRATED = 10
        EMOTE_DRIVE = 11
        EMOTE_EXCITED = 12
        EMOTE_SEARCH = 13
        EMOTE_SHORT_CIRCUIT = 14
        EMOTE_LAUGH = 15
        EMOTE_NO = 16
        EMOTE_RETREAT = 17
        EMOTE_FIERY = 18
        EMOTE_UNDERSTOOD = 19
        EMOTE_YES = 21
        EMOTE_SCAN = 22
        EMOTE_SURPRISED = 24
        IDLE_1 = 25
        IDLE_2 = 26
        IDLE_3 = 27
        WWM_ANGRY = 31
        WWM_ANXIOUS = 32
        WWM_BOW = 33
        WWM_CONCERN = 34
        WWM_CURIOUS = 35
        WWM_DOUBLE_TAKE = 36
        WWM_EXCITED = 37
        WWM_FIERY = 38
        WMM_FRUSTRATED = 39
        WWM_HAPPY = 40
        WWM_JITTERY = 41
        WWM_LAUGH = 42
        WWM_LONG_SHAKE = 43
        WWM_NO = 44
        WWM_OMINOUS = 45
        WWM_RELIEVED = 46
        WWM_SAD = 47
        WWM_SCARED = 48
        WWM_SHAKE = 49
        WWM_SURPRISED = 50
        WWM_TAUNTING = 51
        WWM_WHISPER = 52
        WWM_YELLING = 53
        WWM_YOOHOO = 54
        MOTOR = 55

    sensors = OrderedDict(
        quaternion=OrderedDict(
            x=ToySensor(0x2000000, -1., 1.),
            y=ToySensor(0x1000000, -1., 1.),
            z=ToySensor(0x800000, -1., 1.),
            w=ToySensor(0x400000, -1., 1.)
        ),
        attitude=OrderedDict(
            pitch=ToySensor(0x40000, -179., 180.),
            roll=ToySensor(0x20000, -179., 180.),
            yaw=ToySensor(0x10000, -179., 180.)
        ),
        accelerometer=OrderedDict(
            x=ToySensor(0x8000, -8.19, 8.19),
            y=ToySensor(0x4000, -8.19, 8.19),
            z=ToySensor(0x2000, -8.19, 8.19)
        ),
        accel_one=OrderedDict(accel_one=ToySensor(0x200, 0., 8000.)),
        locator=OrderedDict(
            x=ToySensor(0x40, -32768., 32767., lambda x: x * 100.),
            y=ToySensor(0x20, -32768., 32767., lambda x: x * 100.),
        ),
        velocity=OrderedDict(
            x=ToySensor(0x10, -32768., 32767., lambda x: x * 100.),
            y=ToySensor(0x8, -32768., 32767., lambda x: x * 100.),
        ),
        speed=OrderedDict(speed=ToySensor(0x4, 0., 32767.)),
        core_time=OrderedDict(core_time=ToySensor(0x2, 0., 0.))
    )

    extended_sensors = OrderedDict(
        r2_head_angle=OrderedDict(r2_head_angle=ToySensor(0x4000000, -162., 182.)),
        gyroscope=OrderedDict(
            x=ToySensor(0x2000000, -20000., 20000.),
            y=ToySensor(0x1000000, -20000., 20000.),
            z=ToySensor(0x800000, -20000., 20000.)
        )
    )

    ping = ApiAndShell.ping
    get_api_protocol_version = ApiAndShell.get_api_protocol_version
    send_command_to_shell = ApiAndShell.send_command_to_shell
    add_send_string_to_console_listener = partialmethod(Toy._add_listener, ApiAndShell.send_string_to_console)
    remove_send_string_to_console_listener = partialmethod(Toy._remove_listener, ApiAndShell.send_string_to_console)

    get_main_app_version = SystemInfo.get_main_app_version
    get_bootloader_version = SystemInfo.get_bootloader_version
    get_board_revision = SystemInfo.get_board_revision
    get_mac_address = SystemInfo.get_mac_address
    get_stats_id = SystemInfo.get_stats_id
    get_secondary_main_app_version = SystemInfo.get_secondary_main_app_version
    get_processor_name = SystemInfo.get_processor_name
    get_secondary_mcu_bootloader_version = SystemInfo.get_secondary_mcu_bootloader_version
    get_three_character_sku = SystemInfo.get_three_character_sku

    enter_deep_sleep = Power.enter_deep_sleep
    sleep = Power.sleep
    get_battery_voltage = Power.get_battery_voltage
    get_battery_state = Power.get_battery_state
    enable_battery_state_changed_notify = Power.enable_battery_state_changed_notify
    add_battery_state_changed_notify_listener = partialmethod(Toy._add_listener, Power.battery_state_changed_notify)
    remove_battery_state_changed_notify_listener = partialmethod(Toy._remove_listener,
                                                                 Power.battery_state_changed_notify)

    wake = Power.wake
    get_battery_voltage_state = Power.get_battery_voltage_state
    add_will_sleep_notify_listener = partialmethod(Toy._add_listener, Power.will_sleep_notify)
    remove_will_sleep_notify_listener = partialmethod(Toy._remove_listener, Power.will_sleep_notify)
    add_did_sleep_notify_listener = partialmethod(Toy._add_listener, Power.did_sleep_notify)
    remove_did_sleep_notify_listener = partialmethod(Toy._remove_listener, Power.did_sleep_notify)
    enable_battery_voltage_state_change_notify = Power.enable_battery_voltage_state_change_notify
    add_battery_voltage_state_change_notify_listener = partialmethod(Toy._add_listener,
                                                                     Power.battery_voltage_state_change_notify)
    remove_battery_voltage_state_change_notify_listener = partialmethod(Toy._remove_listener,
                                                                        Power.battery_voltage_state_change_notify)

    set_raw_motors = Drive.set_raw_motors
    reset_yaw = Drive.reset_yaw
    drive_with_heading = Drive.drive_with_heading
    generic_raw_motor = Drive.generic_raw_motor
    set_stabilization = Drive.set_stabilization
    play_animation = Animatronic.play_animation
    perform_leg_action = Animatronic.perform_leg_action
    set_head_position = Animatronic.set_head_position
    get_head_position = Animatronic.get_head_position
    set_leg_position = Animatronic.set_leg_position
    get_leg_position = Animatronic.get_leg_position
    get_leg_action = Animatronic.get_leg_action
    enable_leg_action_notify = Animatronic.enable_leg_action_notify
    stop_animation = Animatronic.stop_animation
    enable_idle_animations = Animatronic.enable_idle_animations
    enable_trophy_mode = Animatronic.enable_trophy_mode
    get_trophy_mode_enabled = Animatronic.get_trophy_mode_enabled
    enable_head_reset_to_zero_notify = Animatronic.enable_head_reset_to_zero_notify
    add_head_reset_to_zero_notify_listener = partialmethod(Toy._add_listener, Animatronic.head_reset_to_zero_notify)
    remove_head_reset_to_zero_notify_listener = partialmethod(Toy._remove_listener,
                                                              Animatronic.head_reset_to_zero_notify)

    set_sensor_streaming_mask = Sensor.set_sensor_streaming_mask
    get_sensor_streaming_mask = Sensor.get_sensor_streaming_mask
    add_sensor_streaming_data_notify_listener = partialmethod(Toy._add_listener, Sensor.sensor_streaming_data_notify)
    remove_sensor_streaming_data_notify_listener = partialmethod(Toy._remove_listener,
                                                                 Sensor.sensor_streaming_data_notify)
    set_extended_sensor_streaming_mask = Sensor.set_extended_sensor_streaming_mask
    get_extended_sensor_streaming_mask = Sensor.get_extended_sensor_streaming_mask
    enable_gyro_max_notify = Sensor.enable_gyro_max_notify
    add_gyro_max_notify_listener = partialmethod(Toy._add_listener, Sensor.gyro_max_notify)
    remove_gyro_max_notify_listener = partialmethod(Toy._remove_listener, Sensor.gyro_max_notify)
    configure_collision_detection = Sensor.configure_collision_detection
    add_collision_detected_notify_listener = partialmethod(Toy._add_listener, Sensor.collision_detected_notify)
    remove_collision_detected_notify_listener = partialmethod(Toy._remove_listener, Sensor.collision_detected_notify)
    reset_locator_x_and_y = Sensor.reset_locator_x_and_y
    set_locator_flags = Sensor.set_locator_flags
    set_accelerometer_activity_threshold = Sensor.set_accelerometer_activity_threshold
    enable_accelerometer_activity_notify = Sensor.enable_accelerometer_activity_notify
    add_accelerometer_activity_notify_listener = partialmethod(Toy._add_listener, Sensor.accelerometer_activity_notify)
    remove_accelerometer_activity_notify_listener = partialmethod(Toy._remove_listener,
                                                                  Sensor.accelerometer_activity_notify)
    set_gyro_activity_threshold = Sensor.set_gyro_activity_threshold
    enable_gyro_activity_notify = Sensor.enable_gyro_activity_notify
    add_gyro_activity_notify_listener = partialmethod(Toy._add_listener, Sensor.gyro_activity_notify)
    remove_gyro_activity_notify_listener = partialmethod(Toy._remove_listener, Sensor.gyro_activity_notify)

    set_bluetooth_name = Connection.set_bluetooth_name
    get_bluetooth_name = Connection.get_bluetooth_name

    play_audio_file = IO.play_audio_file
    set_audio_volume = IO.set_audio_volume
    get_audio_volume = IO.get_audio_volume
    stop_all_audio = IO.stop_all_audio
    set_all_leds_with_16_bit_mask = IO.set_all_leds_with_16_bit_mask
    start_idle_led_animation = IO.start_idle_led_animation

    get_pending_update_flags = Firmware.get_pending_update_flags

    get_factory_mode_challenge = FactoryTest.get_factory_mode_challenge
    enter_factory_mode = FactoryTest.enter_factory_mode
    exit_factory_mode = FactoryTest.exit_factory_mode

    @property
    @lru_cache(None)
    def drive_control(self):
        return DriveControl(self)

    @property
    @lru_cache(None)
    def multi_led_control(self):
        return LedControl(self)

    @property
    @lru_cache(None)
    def sensor_control(self):
        return SensorControl(self)
