// SPDX-License-Identifier: Apache-2.0
#include "rgb_badge/color_transform.h"

namespace rgb_badge {
namespace {

std::uint16_t scale(std::uint16_t linear, std::uint16_t balance,
                    std::uint16_t brightness) noexcept {
    constexpr std::uint64_t denominator = 65535ULL * 65535ULL;
    // At most 65535^3 (< 2^48); round once after both attenuation factors.
    const std::uint64_t numerator = std::uint64_t{linear} * balance * brightness;
    return static_cast<std::uint16_t>((numerator + denominator / 2) / denominator);
}

}  // namespace

ColorTransform::ColorTransform(const GammaTable& gamma, WhiteBalance balance,
                               std::uint16_t brightness) noexcept
    : gamma_(gamma), balance_(balance), brightness_(brightness) {}

std::optional<ColorTransform> ColorTransform::create(const GammaTable& gamma,
                                                    WhiteBalance balance,
                                                    std::uint16_t brightness) noexcept {
    if (gamma.front() != 0 || gamma.back() != 65535) {
        return std::nullopt;
    }
    for (std::size_t i = 1; i < gamma.size(); ++i) {
        if (gamma[i] < gamma[i - 1]) {
            return std::nullopt;
        }
    }
    return ColorTransform(gamma, balance, brightness);
}

Rgb16 ColorTransform::convert(Rgb8 source) const noexcept {
    return {scale(gamma_[source.red], balance_.red, brightness_),
            scale(gamma_[source.green], balance_.green, brightness_),
            scale(gamma_[source.blue], balance_.blue, brightness_)};
}

}  // namespace rgb_badge
