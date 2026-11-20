// SPDX-License-Identifier: Apache-2.0
#pragma once

#include "rgb_badge/color_transform.h"

namespace rgb_badge {

constexpr std::size_t kAssetMaxBytes = 16U * 1024U * 1024U;
constexpr std::uint32_t kAssetMaxDecodedPixels = 16000000U;
constexpr unsigned kAssetKeyframeInterval = 60;

enum class AssetError {
    None, InvalidArgument, Truncated, TooLarge, BadMagic, UnsupportedVersion,
    BadHeader, UnsupportedDimensions, ExpansionLimit, BadBodyChecksum,
    BadFrame, BadFrameChecksum, InsufficientOutput, OverlappingOutput,
    DurationMismatch, TrailingData, MissingReference
};

struct AssetInfo {
    std::uint16_t width;
    std::uint16_t height;
    std::uint32_t frame_count;
    std::uint64_t duration_us;
    std::uint16_t version = 1;
};

enum class DecodeStatus { Frame, End, Error };

struct DecodeResult {
    DecodeStatus status;
    AssetError error;
    std::uint32_t frame_index;
    std::uint32_t duration_us;
};

// IEEE CRC-32 over a valid byte span; nullptr is permitted only for size zero.
std::uint32_t crc32_ieee(const std::uint8_t* bytes, std::size_t size) noexcept;

class AssetReader {
public:
    // Borrowed bytes must remain alive and unchanged. No heap allocation.
    static std::optional<AssetReader> open(const std::uint8_t* bytes,
                                           std::size_t size, AssetError& error) noexcept;
    const AssetInfo& info() const noexcept { return info_; }
    DecodeResult next(Rgb8* output, std::size_t pixel_capacity) noexcept;
    void rewind() noexcept {
        offset_ = 32; frame_index_ = 0; reference_valid_ = false; delta_run_ = 0;
    }

private:
    AssetReader(const std::uint8_t* bytes, std::size_t size, AssetInfo info) noexcept
        : bytes_(bytes), size_(size), info_(info) {}

    const std::uint8_t* bytes_;
    std::size_t size_;
    AssetInfo info_;
    std::size_t offset_ = 32;
    std::uint32_t frame_index_ = 0;
    // Independent of caller output buffers; bounded object storage, no heap.
    std::array<Rgb8, 768> reference_{};
    bool reference_valid_ = false;
    unsigned delta_run_ = 0;
};

}  // namespace rgb_badge
