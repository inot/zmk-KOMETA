target_sources(app PRIVATE src/behaviors/behavior_turbo.c)

if(CONFIG_ZMK_SPLIT AND NOT CONFIG_ZMK_SPLIT_ROLE_CENTRAL)
  target_sources(app PRIVATE src/events/keycode_state_changed.c)
endif()
