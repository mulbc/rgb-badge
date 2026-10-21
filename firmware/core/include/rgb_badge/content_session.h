// SPDX-License-Identifier: Apache-2.0
#pragma once

#include "rgb_badge/asset_playback.h"
#include "rgb_badge/mode_button.h"

namespace rgb_badge {

enum class SessionState { AwaitRelease, Ready, Playing, Inhibited, Complete, Programming, Fault };
enum class SessionCommand { None, Start, Stop };
enum class SessionFault { None, ModeClock, Playback };

struct SessionResult {
    SessionState state = SessionState::AwaitRelease;
    SessionFault fault = SessionFault::None;
    ModeEvent mode_event = ModeEvent::None;
    PlaybackResult playback{};
    bool command_accepted = false;
    bool frame_ready = false;
    bool ble_requested = false;
    // False is software eligibility only, never hardware-arm permission.
    bool display_inhibit = true;
};

class ContentSession {
public:
    static std::optional<ContentSession> create(const AssetReader& reader,
                                               const ColorTransform& transform,
                                               ModeButtonConfig button = {},
                                               std::uint32_t max_lateness_us = 0) noexcept;
    SessionResult step(std::uint64_t now_us, bool pressed,
                       SessionCommand command = SessionCommand::None) noexcept;
    void reset() noexcept;
    const Rgb16* pixels() const noexcept { return output_.data(); }
    std::size_t pixel_count() const noexcept { return playback_.pixel_count(); }
    const AssetInfo& info() const noexcept { return playback_.info(); }
    std::uint16_t brightness() const noexcept { return transform_.brightness(); }

private:
    ContentSession(const AssetReader& reader, const ColorTransform& transform,
                   const ModeButton& button, std::uint32_t max_lateness_us) noexcept
        : playback_(reader, max_lateness_us), transform_(transform), button_(button) {}
    void stop_output() noexcept;
    SessionResult fail(SessionFault fault) noexcept;

    AssetPlayback playback_;
    ColorTransform transform_;
    ModeButton button_;
    std::array<Rgb16, 768> output_{};
    SessionResult result_{};
};

} // namespace rgb_badge
