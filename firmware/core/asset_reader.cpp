// SPDX-License-Identifier: Apache-2.0
#include "rgb_badge/asset_reader.h"

#include <algorithm>

namespace rgb_badge {
namespace {

constexpr auto crc_table() noexcept {
    std::array<std::uint32_t, 256> result{};
    for (std::uint32_t i = 0; i < result.size(); ++i) {
        auto state = i;
        for (unsigned bit = 0; bit < 8; ++bit) {
            state = (state >> 1) ^ ((state & 1) ? 0xedb88320U : 0U);
        }
        result[i] = state;
    }
    return result;
}
constexpr auto kCrc = crc_table();

std::uint32_t update_crc(std::uint32_t state, std::uint8_t byte) noexcept {
    return kCrc[(state ^ byte) & 255U] ^ (state >> 8);
}

std::uint16_t u16(const std::uint8_t* q) noexcept {
    return static_cast<std::uint16_t>(q[0] | (std::uint16_t{q[1]} << 8));
}

std::uint32_t u32(const std::uint8_t* q) noexcept {
    return std::uint32_t{q[0]} | (std::uint32_t{q[1]} << 8) |
           (std::uint32_t{q[2]} << 16) | (std::uint32_t{q[3]} << 24);
}

std::uint64_t u64(const std::uint8_t* q) noexcept {
    return u32(q) | (std::uint64_t{u32(q + 4)} << 32);
}

struct Frame {
    const std::uint8_t* payload = nullptr;
    std::size_t length = 0;
    std::size_t next = 0;
    std::uint32_t duration = 0;
    std::uint32_t checksum = 0;
    std::uint16_t palette_count = 0;
    std::uint8_t codec = 0;
};

AssetError parse_frame(const std::uint8_t* bytes, std::size_t size, std::size_t offset,
                       std::size_t pixels, Frame& frame) noexcept {
    if (offset > size || size - offset < 16) return AssetError::Truncated;
    const auto* header = bytes + offset;
    frame.duration = u32(header);
    frame.codec = header[4];
    frame.palette_count = u16(header + 6);
    frame.length = u32(header + 8);
    frame.checksum = u32(header + 12);
    if (frame.duration == 0 || header[5] != 0 || frame.codec > 2) return AssetError::BadFrame;
    if (frame.length > size - offset - 16) return AssetError::Truncated;
    frame.payload = header + 16;
    frame.next = offset + 16 + frame.length;
    if (frame.codec == 0) {
        return frame.palette_count == 0 && frame.length == pixels * 3
                   ? AssetError::None : AssetError::BadFrame;
    }
    std::size_t start = 0;
    const std::size_t stride = frame.codec == 1 ? 4 : 2;
    if (frame.codec == 1) {
        if (frame.palette_count != 0) return AssetError::BadFrame;
    } else {
        if (frame.palette_count == 0 || frame.palette_count > 256) return AssetError::BadFrame;
        start = frame.palette_count * 3U;
    }
    if (start > frame.length || (frame.length - start) % stride != 0) return AssetError::BadFrame;
    std::size_t decoded = 0;
    for (std::size_t i = start; i < frame.length; i += stride) {
        const std::size_t count = std::size_t{frame.payload[i]} + 1;
        if (count > pixels - decoded) return AssetError::BadFrame;
        if (frame.codec == 2 && frame.payload[i + 1] >= frame.palette_count) return AssetError::BadFrame;
        decoded += count;
    }
    return decoded == pixels ? AssetError::None : AssetError::BadFrame;
}

bool overlaps(const std::uint8_t* input, std::size_t size,
               const Rgb8* output, std::size_t pixels) noexcept {
    const auto a = reinterpret_cast<std::uintptr_t>(input);
    const auto b = reinterpret_cast<std::uintptr_t>(output);
    return b <= a ? a - b < pixels * sizeof(Rgb8) : b - a < size;
}

}  // namespace

std::uint32_t crc32_ieee(const std::uint8_t* bytes, std::size_t size) noexcept {
    std::uint32_t state = 0xffffffffU;
    for (std::size_t i = 0; i < size; ++i) state = update_crc(state, bytes[i]);
    return state ^ 0xffffffffU;
}

std::optional<AssetReader> AssetReader::open(const std::uint8_t* bytes,
                                             std::size_t size, AssetError& error) noexcept {
    const auto fail = [&error](AssetError reason) -> std::optional<AssetReader> {
        error = reason;
        return std::nullopt;
    };
    if (bytes == nullptr) return fail(AssetError::InvalidArgument);
    if (size > kAssetMaxBytes) return fail(AssetError::TooLarge);
    if (size < 32) return fail(AssetError::Truncated);
    if (bytes[0] != 'R' || bytes[1] != 'G' || bytes[2] != 'B' || bytes[3] != 'B') return fail(AssetError::BadMagic);
    if (u16(bytes + 4) != 1) return fail(AssetError::UnsupportedVersion);
    if (u16(bytes + 6) != 32 || u32(bytes + 12) == 0) return fail(AssetError::BadHeader);
    const AssetInfo info{u16(bytes + 8), u16(bytes + 10), u32(bytes + 12), u64(bytes + 16)};
    if ((info.width != 16 && info.width != 48) || info.height != 16) return fail(AssetError::UnsupportedDimensions);
    const std::size_t pixels = info.width * info.height;
    if (info.frame_count > kAssetMaxDecodedPixels / pixels) return fail(AssetError::ExpansionLimit);
    if (u32(bytes + 24) != size - 32) return fail(AssetError::BadHeader);
    if (u32(bytes + 28) != crc32_ieee(bytes + 32, size - 32)) return fail(AssetError::BadBodyChecksum);
    std::size_t offset = 32;
    std::uint64_t duration = 0;
    for (std::uint32_t i = 0; i < info.frame_count; ++i) {
        Frame frame;
        const auto result = parse_frame(bytes, size, offset, pixels, frame);
        if (result != AssetError::None) return fail(result);
        duration += frame.duration;  // Bounded frame count makes overflow impossible.
        offset = frame.next;
    }
    if (offset != size) return fail(AssetError::TrailingData);
    if (duration != info.duration_us) return fail(AssetError::DurationMismatch);
    error = AssetError::None;
    return AssetReader(bytes, size, info);
}

DecodeResult AssetReader::next(Rgb8* output, std::size_t pixel_capacity) noexcept {
    const auto fail = [this](AssetError error) {
        return DecodeResult{DecodeStatus::Error, error, frame_index_, 0};
    };
    if (frame_index_ == info_.frame_count) return {DecodeStatus::End, AssetError::None, frame_index_, 0};
    const std::size_t pixels = info_.width * info_.height;
    if (output == nullptr) return fail(AssetError::InvalidArgument);
    if (pixel_capacity < pixels) return fail(AssetError::InsufficientOutput);
    if (overlaps(bytes_, size_, output, pixels)) return fail(AssetError::OverlappingOutput);
    Frame frame;
    const auto result = parse_frame(bytes_, size_, offset_, pixels, frame);
    if (result != AssetError::None) return fail(result);
    if (frame.codec == 0) {
        for (std::size_t i = 0; i < pixels; ++i) {
            output[i] = {frame.payload[3*i], frame.payload[3*i+1], frame.payload[3*i+2]};
        }
    } else {
        const std::size_t start = frame.codec == 1 ? 0 : frame.palette_count * 3U;
        const std::size_t stride = frame.codec == 1 ? 4 : 2;
        std::size_t at = 0;
        for (std::size_t i = start; i < frame.length; i += stride) {
            const auto* rgb = frame.codec == 1 ? frame.payload + i + 1
                                              : frame.payload + 3U * frame.payload[i+1];
            const Rgb8 color{rgb[0], rgb[1], rgb[2]};
            for (unsigned j = 0; j <= frame.payload[i]; ++j) output[at++] = color;
        }
    }
    auto checksum = 0xffffffffU;
    for (std::size_t i = 0; i < pixels; ++i) {
        checksum = update_crc(checksum, output[i].red);
        checksum = update_crc(checksum, output[i].green);
        checksum = update_crc(checksum, output[i].blue);
    }
    if ((checksum ^ 0xffffffffU) != frame.checksum) {
        std::fill_n(output, pixels, Rgb8{0, 0, 0});
        return fail(AssetError::BadFrameChecksum);
    }
    offset_ = frame.next;
    return {DecodeStatus::Frame, AssetError::None, frame_index_++, frame.duration};
}

}  // namespace rgb_badge
