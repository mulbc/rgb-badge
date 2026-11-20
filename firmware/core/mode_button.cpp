// SPDX-License-Identifier: Apache-2.0
#include "rgb_badge/mode_button.h"

namespace rgb_badge {

std::optional<ModeButton> ModeButton::create(ModeButtonConfig config) noexcept {
    if (!config.debounce_us || config.hold_us < config.debounce_us) return std::nullopt;
    return ModeButton(config);
}

ModeResult ModeButton::result(ModeEvent event) const noexcept {
    return {state_, event, error_, state_ == ModeState::Programming,
            state_ != ModeState::Playback || release_inhibit_};
}

void ModeButton::reset() noexcept {
    state_ = ModeState::AwaitRelease;
    error_ = ModeError::None;
    initialized_ = false;
    candidate_pressed_ = stable_pressed_ = true;
    release_inhibit_ = true;
    last_update_us_ = candidate_since_us_ = press_since_us_ = 0;
}

ModeResult ModeButton::update(std::uint64_t now_us, bool pressed) noexcept {
    if (state_ == ModeState::Fault) return result();
    if (initialized_ && now_us < last_update_us_) {
        state_ = ModeState::Fault;
        error_ = ModeError::ClockReversed;
        return result(ModeEvent::ClockFault);
    }
    last_update_us_ = now_us;
    if (!initialized_ || candidate_pressed_ != pressed) {
        candidate_pressed_ = pressed;
        candidate_since_us_ = now_us;
    }
    initialized_ = true;
    const bool qualified = now_us - candidate_since_us_ >= config_.debounce_us;
    // Even a press too short to qualify must inhibit until release qualifies.
    if (pressed) release_inhibit_ = true;
    else if (qualified) release_inhibit_ = false;
    if (qualified && stable_pressed_ != candidate_pressed_) {
        stable_pressed_ = candidate_pressed_;
        // Addition is bounded by now_us because the elapsed interval qualified.
        press_since_us_ = stable_pressed_ ? candidate_since_us_ + config_.debounce_us : 0;
    }
    if (state_ == ModeState::AwaitRelease && qualified && !stable_pressed_) {
        state_ = ModeState::Playback;
        return result(ModeEvent::PlaybackReady);
    }
    if (state_ == ModeState::Playback && qualified && stable_pressed_ && candidate_pressed_ &&
        now_us - press_since_us_ >= config_.hold_us) {
        state_ = ModeState::Programming;
        return result(ModeEvent::EnterProgramming);
    }
    return result();
}

} // namespace rgb_badge
