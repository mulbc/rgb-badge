// SPDX-License-Identifier: Apache-2.0
#pragma once

#include <array>
#include <cstddef>
#include <cstdint>
#include <optional>

namespace rgb_badge {

struct Rgb8 {
    std::uint8_t red;
    std::uint8_t green;
    std::uint8_t blue;
};

// Normalized linear intensities, not driver register words or current settings.
struct Rgb16 {
    std::uint16_t red;
    std::uint16_t green;
    std::uint16_t blue;
};

using GammaTable = std::array<std::uint16_t, 256>;

// UNORM16 attenuation: 0 is off, 65535 is unity. No channel amplification.
struct WhiteBalance {
    std::uint16_t red;
    std::uint16_t green;
    std::uint16_t blue;
};

constexpr GammaTable identity_gamma() noexcept {
    GammaTable result{};
    for (std::size_t i = 0; i < result.size(); ++i) {
        result[i] = static_cast<std::uint16_t>(i * 257U);
    }
    return result;
}

class ColorTransform {
public:
    // Reject a table unless black is zero, white is 65535 and it is monotonic.
    // Copy settings at creation; later changes to the caller's table have no
    // effect. Brightness changes require an explicit replacement transform.
    static std::optional<ColorTransform> create(const GammaTable& gamma,
                                                WhiteBalance balance,
                                                std::uint16_t brightness) noexcept;

    Rgb16 convert(Rgb8 source) const noexcept;
    std::uint16_t brightness() const noexcept { return brightness_; }

private:
    ColorTransform(const GammaTable& gamma, WhiteBalance balance,
                   std::uint16_t brightness) noexcept;

    GammaTable gamma_;
    WhiteBalance balance_;
    std::uint16_t brightness_;
};

}  // namespace rgb_badge
