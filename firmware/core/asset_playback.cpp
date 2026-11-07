// SPDX-License-Identifier: Apache-2.0
#include "rgb_badge/asset_playback.h"

#include <limits>

namespace rgb_badge {

PlaybackResult AssetPlayback::fail(PlaybackError error, AssetError asset_error) noexcept {
    clear();
    result_.status = PlaybackStatus::Error;
    result_.error = error;
    result_.asset_error = asset_error;
    return result_;
}

void AssetPlayback::stop() noexcept {
    clear();
    reader_.rewind();
    last_poll_us_ = 0;
    result_ = {};
}

PlaybackResult AssetPlayback::start(std::uint64_t now_us) noexcept {
    stop();
    // Validate the entire one-shot timeline before adding any frame duration.
    if (reader_.info().duration_us > std::numeric_limits<std::uint64_t>::max() - now_us) {
        return fail(PlaybackError::TimeOverflow);
    }
    last_poll_us_ = now_us;
    return decode(now_us, 0);
}

PlaybackResult AssetPlayback::decode(std::uint64_t scheduled_start_us,
                                     std::uint64_t lateness_us) noexcept {
    const auto decoded = reader_.next(output_.data(), output_.size());
    if (decoded.status != DecodeStatus::Frame) {
        return fail(PlaybackError::DecodeFailure, decoded.error);
    }
    result_ = {PlaybackStatus::Frame, PlaybackError::None, AssetError::None,
               decoded.frame_index, decoded.duration_us, scheduled_start_us,
               scheduled_start_us + decoded.duration_us, lateness_us};
    // Even a large caller-supplied budget cannot admit an entirely expired frame.
    if (lateness_us >= decoded.duration_us) return fail(PlaybackError::DeadlineMiss);
    return result_;
}

PlaybackResult AssetPlayback::poll(std::uint64_t now_us) noexcept {
    if (result_.status == PlaybackStatus::Idle || result_.status == PlaybackStatus::End ||
        result_.status == PlaybackStatus::Error) return result_;
    if (now_us < last_poll_us_) return fail(PlaybackError::ClockReversed);
    last_poll_us_ = now_us;
    if (now_us < result_.scheduled_end_us) {
        result_.status = PlaybackStatus::Waiting;
        return result_;
    }
    const auto boundary = result_.scheduled_end_us;
    const auto lateness = now_us - boundary;
    result_.lateness_us = lateness;
    if (lateness > max_lateness_us_) return fail(PlaybackError::DeadlineMiss);
    if (result_.frame_index + 1 == reader_.info().frame_count) {
        clear();
        result_.status = PlaybackStatus::End;
        return result_;
    }
    return decode(boundary, lateness);
}

}  // namespace rgb_badge
