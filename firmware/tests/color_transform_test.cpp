// SPDX-License-Identifier: Apache-2.0
#include "rgb_badge/color_transform.h"

#include <cstdlib>
#include <iostream>

namespace {
unsigned checks = 0;

void expect(bool condition, const char* message) {
    ++checks;
    if (!condition) {
        std::cerr << "FAIL: " << message << '\n';
        std::exit(EXIT_FAILURE);
    }
}

bool equal(rgb_badge::Rgb16 a, rgb_badge::Rgb16 b) {
    return a.red == b.red && a.green == b.green && a.blue == b.blue;
}
}  // namespace

int main() {
    using namespace rgb_badge;
    constexpr WhiteBalance unity{65535, 65535, 65535};
    auto gamma = identity_gamma();
    const auto identity = ColorTransform::create(gamma, unity, 65535);
    expect(identity.has_value(), "identity table accepted");
    for (unsigned i = 0; i < 256; ++i) {
        const auto byte = static_cast<std::uint8_t>(i);
        const auto word = static_cast<std::uint16_t>(i * 257);
        expect(equal(identity->convert({byte, byte, byte}), {word, word, word}),
               "full intensity maps every 8-bit value exactly to UNORM16");
        expect(equal(identity->convert({byte, 0, 0}), {word, 0, 0}),
               "red has no cross-channel leakage");
        expect(equal(identity->convert({0, byte, 0}), {0, word, 0}),
               "green has no cross-channel leakage");
        expect(equal(identity->convert({0, 0, byte}), {0, 0, word}),
               "blue has no cross-channel leakage");
    }

    const auto off = ColorTransform::create(gamma, unity, 0);
    const auto balanced = ColorTransform::create(gamma, {32768, 65535, 0}, 32768);
    expect(off.has_value() && balanced.has_value(), "attenuation settings accepted");
    expect(equal(balanced->convert({255, 255, 255}), {16384, 32768, 0}),
           "white balance and fixed brightness use the expected rounded intensities");
    expect(equal(balanced->convert({1, 1, 1}), {64, 129, 0}),
           "round only once: staged rounding would incorrectly produce red 65");
    expect(balanced->brightness() == 32768, "brightness remains the requested setting");

    std::uint16_t last = 0;
    for (unsigned i = 0; i < 256; ++i) {
        const auto byte = static_cast<std::uint8_t>(i);
        expect(equal(off->convert({byte, byte, byte}), {0, 0, 0}),
               "brightness zero blanks every source level");
        const auto output = balanced->convert({byte, byte, byte});
        expect(output.red <= output.green && output.green <= i * 257 && output.blue == 0,
               "attenuation cannot amplify an input or revive a disabled channel");
        expect(output.red >= last, "attenuation preserves the monotonic ramp");
        last = output.red;
    }
    expect(equal(balanced->convert({0, 0, 0}), {0, 0, 0}), "black stays black");

    // Synthetic gamma 2.0, solely for a software test. Not optical calibration.
    GammaTable curved{};
    for (std::uint64_t i = 0; i < curved.size(); ++i) {
        curved[i] = static_cast<std::uint16_t>((i * i * 65535 + 32512) / 65025);
    }
    const auto quadratic = ColorTransform::create(curved, unity, 65535);
    expect(quadratic.has_value(), "nonlinear monotonic table accepted");
    expect(equal(quadratic->convert({51, 102, 153}), {2621, 10486, 23593}),
           "independent fifth-scale gamma 2.0 golden values");
    expect(equal(quadratic->convert({204, 255, 0}), {41942, 65535, 0}),
           "gamma golden values include black and white endpoints");
    const auto quadratic_dimmed = ColorTransform::create(curved, unity, 32768);
    expect(quadratic_dimmed.has_value(), "nonlinear fixed-brightness table accepted");
    expect(equal(quadratic_dimmed->convert({51, 102, 153}), {1311, 5243, 11797}),
           "brightness scales linear output after gamma, not encoded source bytes");

    gamma[128] = 0;
    expect(!ColorTransform::create(gamma, unity, 65535), "decreasing LUT rejected");
    expect(equal(identity->convert({128, 128, 128}), {32896, 32896, 32896}),
           "caller mutation does not alter an existing transform");
    gamma = identity_gamma();
    gamma[0] = 1;
    expect(!ColorTransform::create(gamma, unity, 65535), "nonzero black rejected");
    gamma = identity_gamma();
    gamma[255] = 65534;
    expect(!ColorTransform::create(gamma, unity, 65535), "incomplete full scale rejected");
    expect(!ColorTransform::create(GammaTable{}, unity, 65535), "empty table rejected");
    GammaTable stepped{};
    stepped.back() = 65535;
    expect(ColorTransform::create(stepped, unity, 65535).has_value(),
           "monotonic tables may contain plateaus");

    // Worst-case numerator also checks the wide arithmetic under sanitizers.
    expect(equal(identity->convert({255, 255, 255}), {65535, 65535, 65535}),
           "full-scale arithmetic does not overflow");
    std::cout << "Color transform: " << checks << " checks passed\n";
}
