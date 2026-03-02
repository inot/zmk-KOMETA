/*
 * Copyright (c) 2020 The ZMK Contributors
 *
 * SPDX-License-Identifier: MIT
 */

#define DT_DRV_COMPAT zmk_behavior_turbo

#include <errno.h>
#include <zephyr/device.h>
#include <zephyr/devicetree.h>
#include <zephyr/kernel.h>
#include <zephyr/logging/log.h>
#include <zephyr/random/random.h>

#include <drivers/behavior.h>
#include <zmk/behavior.h>
#include <zmk/event_manager.h>
#include <zmk/events/keycode_state_changed.h>
#include <zmk/keymap.h>

LOG_MODULE_DECLARE(zmk, CONFIG_ZMK_LOG_LEVEL);

#define TURBO_REPEAT_MS 333
#define TURBO_TAP_MS 20
#define TURBO_REPEAT_JITTER_MS 50
#define TURBO_TAP_JITTER_MS 8
#define TURBO_POSITIONS                                                                            \
    (DT_PROP(DT_NODELABEL(default_transform), rows) * DT_PROP(DT_NODELABEL(default_transform), columns))

struct turbo_state {
    struct k_timer timer;
    struct k_work_delayable release_work;
    uint32_t keycode;
    bool active;
};

static struct turbo_state turbo_states[TURBO_POSITIONS];
static bool timers_initialized;

static uint32_t jitter_ms(uint32_t base_ms, uint32_t jitter_ms) {
    if (jitter_ms == 0) {
        return base_ms;
    }

    uint32_t span = (jitter_ms * 2U) + 1U;
    int32_t delta = (int32_t)(sys_rand32_get() % span) - (int32_t)jitter_ms;
    int32_t value = (int32_t)base_ms + delta;

    return (uint32_t)(value < 1 ? 1 : value);
}

static void turbo_release_handler(struct k_work *work) {
    struct k_work_delayable *delayable = k_work_delayable_from_work(work);
    struct turbo_state *state = CONTAINER_OF(delayable, struct turbo_state, release_work);

    if (!state || !state->active) {
        return;
    }

    raise_zmk_keycode_state_changed_from_encoded(state->keycode, false, k_uptime_get());
}

static void turbo_timer_handler(struct k_timer *timer) {
    struct turbo_state *state = k_timer_user_data_get(timer);

    if (!state || !state->active) {
        return;
    }

    int64_t timestamp = k_uptime_get();
    raise_zmk_keycode_state_changed_from_encoded(state->keycode, true, timestamp);
    k_work_reschedule(&state->release_work,
                      K_MSEC(jitter_ms(TURBO_TAP_MS, TURBO_TAP_JITTER_MS)));
    k_timer_start(&state->timer, K_MSEC(jitter_ms(TURBO_REPEAT_MS, TURBO_REPEAT_JITTER_MS)),
                  K_NO_WAIT);
}

static void init_timers(void) {
    for (size_t idx = 0; idx < TURBO_POSITIONS; idx++) {
        k_timer_init(&turbo_states[idx].timer, turbo_timer_handler, NULL);
        k_timer_user_data_set(&turbo_states[idx].timer, &turbo_states[idx]);
        k_work_init_delayable(&turbo_states[idx].release_work, turbo_release_handler);
        turbo_states[idx].active = false;
        turbo_states[idx].keycode = 0;
    }
}

static int behavior_turbo_init(const struct device *dev) {
    ARG_UNUSED(dev);

    if (!timers_initialized) {
        init_timers();
        timers_initialized = true;
    }

    return 0;
}

static int on_keymap_binding_pressed(struct zmk_behavior_binding *binding,
                                     struct zmk_behavior_binding_event event) {
    if (event.position >= TURBO_POSITIONS) {
        return -EINVAL;
    }

    struct turbo_state *state = &turbo_states[event.position];

    state->keycode = binding->param1;
    state->active = true;

    k_timer_stop(&state->timer);

    int64_t timestamp = k_uptime_get();
    raise_zmk_keycode_state_changed_from_encoded(state->keycode, true, timestamp);
    k_work_reschedule(&state->release_work, K_MSEC(TURBO_TAP_MS));

    k_timer_start(&state->timer, K_MSEC(jitter_ms(TURBO_REPEAT_MS, TURBO_REPEAT_JITTER_MS)),
                  K_NO_WAIT);

    return ZMK_BEHAVIOR_OPAQUE;
}

static int on_keymap_binding_released(struct zmk_behavior_binding *binding,
                                      struct zmk_behavior_binding_event event) {
    ARG_UNUSED(binding);

    if (event.position >= TURBO_POSITIONS) {
        return -EINVAL;
    }

    struct turbo_state *state = &turbo_states[event.position];

    state->active = false;
    k_timer_stop(&state->timer);
    k_work_cancel_delayable(&state->release_work);
    raise_zmk_keycode_state_changed_from_encoded(state->keycode, false, k_uptime_get());

    return ZMK_BEHAVIOR_OPAQUE;
}

static const struct behavior_driver_api behavior_turbo_driver_api = {
    .binding_pressed = on_keymap_binding_pressed,
    .binding_released = on_keymap_binding_released,
    .locality = BEHAVIOR_LOCALITY_EVENT_SOURCE,
};

BEHAVIOR_DT_INST_DEFINE(0, behavior_turbo_init, NULL, NULL, NULL, POST_KERNEL,
                        CONFIG_KERNEL_INIT_PRIORITY_DEFAULT, &behavior_turbo_driver_api);
