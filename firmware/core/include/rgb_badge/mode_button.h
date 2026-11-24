// SPDX-License-Identifier: Apache-2.0
#pragma once

#include <cstdint>
#include <optional>

namespace rgb_badge {

struct ModeButtonConfig {
    std::uint32_t debounce_us = 30000;
    std::uint32_t hold_us = 3000000;
};

enum class ModeState { AwaitRelease, Playback, Programming, Fault };
enum class ModeEvent { None, PlaybackReady, EnterProgramming, ClockFault };
enum class ModeError { None, ClockReversed };

struct ModeResult {
    ModeState state;
    ModeEvent event;
    ModeError error;
    bool ble_requested;
    bool display_inhibit;
};

// Logical sampled input only: no GPIO, BLE or hardware display-arm interface.
class ModeButton {
public:
    static std::optional<ModeButton> create(ModeButtonConfig config = {}) noexcept;
    ModeResult update(std::uint64_t now_us, bool pressed) noexcept;
    void reset() noexcept;

private:
    explicit ModeButton(ModeButtonConfig config) noexcept : config_(config) {}
    ModeResult result(ModeEvent event = ModeEvent::None) const noexcept;

    ModeButtonConfig config_;
    ModeState state_ = ModeState::AwaitRelease;
    ModeError error_ = ModeError::None;
    bool initialized_ = false;
    bool candidate_pressed_ = true;
    bool stable_pressed_ = true;
    bool release_inhibit_ = true;
    std::uint64_t last_update_us_ = 0;
    std::uint64_t candidate_since_us_ = 0;
    std::uint64_t press_since_us_ = 0;
};

} // namespace rgb_badge
