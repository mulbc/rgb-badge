// SPDX-License-Identifier: Apache-2.0
#include "rgb_badge/content_session.h"

namespace rgb_badge {

std::optional<ContentSession> ContentSession::create(const AssetReader& reader,
                                                    const ColorTransform& transform,
                                                    ModeButtonConfig config,
                                                    std::uint32_t max_lateness_us) noexcept {
    const auto button = ModeButton::create(config);
    if (!button) return std::nullopt;
    return ContentSession(reader, transform, *button, max_lateness_us);
}

void ContentSession::stop_output() noexcept {
    playback_.stop();
    output_.fill({0, 0, 0});
    result_.frame_ready = false;
    result_.display_inhibit = true;
}

void ContentSession::reset() noexcept {
    stop_output();
    button_.reset();
    result_ = {};
}

SessionResult ContentSession::fail(SessionFault fault) noexcept {
    stop_output();
    result_.state = SessionState::Fault;
    result_.fault = fault;
    result_.ble_requested = false;
    result_.command_accepted = false;
    return result_;
}

SessionResult ContentSession::step(std::uint64_t now_us, bool pressed,
                                   SessionCommand command) noexcept {
    result_.mode_event = ModeEvent::None;
    result_.command_accepted = false;
    result_.frame_ready = false;
    if (result_.state == SessionState::Fault) return result_;
    const auto mode = button_.update(now_us, pressed);
    result_.mode_event = mode.event;
    result_.ble_requested = mode.ble_requested;
    if (mode.state == ModeState::Fault) return fail(SessionFault::ModeClock);
    if (mode.display_inhibit) {
        stop_output();
        result_.playback = {};
        result_.state = mode.state == ModeState::Programming ? SessionState::Programming :
                        mode.state == ModeState::AwaitRelease ? SessionState::AwaitRelease :
                        SessionState::Inhibited;
        return result_;
    }
    if (command == SessionCommand::Stop) {
        stop_output();
        result_.playback = {};
        result_.state = SessionState::Ready;
        result_.command_accepted = true;
        return result_;
    }
    const bool playing = result_.state == SessionState::Playing;
    if (command == SessionCommand::Start && !playing) {
        result_.command_accepted = true;
        result_.playback = playback_.start(now_us);
    } else if (playing) {
        // Repeated Start never rewinds or hides a missed playback deadline.
        result_.playback = playback_.poll(now_us);
    } else {
        if (result_.state != SessionState::Complete) result_.state = SessionState::Ready;
        return result_;
    }
    const auto status = result_.playback.status;
    if (status == PlaybackStatus::Error) return fail(SessionFault::Playback);
    if (status == PlaybackStatus::End) {
        stop_output();
        result_.state = SessionState::Complete;
        return result_;
    }
    if (status == PlaybackStatus::Frame) {
        for (std::size_t i = 0; i < pixel_count(); ++i) output_[i] = transform_.convert(playback_.pixels()[i]);
        result_.frame_ready = true;
    }
    result_.state = SessionState::Playing;
    result_.display_inhibit = false;
    return result_;
}

} // namespace rgb_badge
