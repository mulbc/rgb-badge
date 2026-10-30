// SPDX-License-Identifier: Apache-2.0
#pragma once

#include "rgb_badge/asset_reader.h"

namespace rgb_badge {

enum class PlaybackStatus { Idle, Frame, Waiting, End, Error };
enum class PlaybackError { None, ClockReversed, DeadlineMiss, TimeOverflow, DecodeFailure };

struct PlaybackResult {
    PlaybackStatus status = PlaybackStatus::Idle;
    PlaybackError error = PlaybackError::None;
    AssetError asset_error = AssetError::None;
    std::uint32_t frame_index = 0;
    std::uint32_t duration_us = 0;
    std::uint64_t scheduled_start_us = 0;
    std::uint64_t scheduled_end_us = 0;
    std::uint64_t lateness_us = 0;
};

// One-shot, no-heap host playback. Borrowed asset bytes must remain immutable
// and alive. No GPIO/brightness/rail control; pixels are software output only.
class AssetPlayback {
public:
    explicit AssetPlayback(const AssetReader& reader, std::uint32_t max_lateness_us = 0) noexcept
        : reader_(reader), max_lateness_us_(max_lateness_us) {}

    PlaybackResult start(std::uint64_t now_us) noexcept;
    PlaybackResult poll(std::uint64_t now_us) noexcept;
    void stop() noexcept;

    const AssetInfo& info() const noexcept { return reader_.info(); }
    const Rgb8* pixels() const noexcept { return output_.data(); }
    std::size_t pixel_count() const noexcept {
        return std::size_t{info().width} * info().height;
    }

private:
    PlaybackResult decode(std::uint64_t scheduled_start_us, std::uint64_t lateness_us) noexcept;
    PlaybackResult fail(PlaybackError error, AssetError asset_error = AssetError::None) noexcept;
    void clear() noexcept { output_.fill({0, 0, 0}); }

    AssetReader reader_;
    std::array<Rgb8, 768> output_{};
    std::uint32_t max_lateness_us_;
    std::uint64_t last_poll_us_ = 0;
    PlaybackResult result_{};
};

}  // namespace rgb_badge
