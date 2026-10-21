// SPDX-License-Identifier: Apache-2.0
#include "rgb_badge/asset_reader.h"

#include <cstdlib>
#include <iostream>
#include <vector>

using namespace rgb_badge;
namespace {
unsigned checks = 0;
using Bytes = std::vector<std::uint8_t>;

void expect(bool condition, const char* message) {
    ++checks;
    if (!condition) { std::cerr << "FAIL: " << message << '\n'; std::exit(EXIT_FAILURE); }
}

void put(Bytes& bytes, std::size_t offset, std::uint64_t value, unsigned width) {
    for (unsigned i = 0; i < width; ++i) bytes[offset + i] = static_cast<std::uint8_t>(value >> (8*i));
}

void seal(Bytes& bytes) {
    put(bytes, 24, bytes.size() - 32, 4);
    put(bytes, 28, crc32_ieee(bytes.data() + 32, bytes.size() - 32), 4);
}

Bytes asset(unsigned codec, unsigned palette, const Bytes& payload, const Bytes& decoded) {
    Bytes bytes(48, 0);
    bytes[0] = 'R'; bytes[1] = 'G'; bytes[2] = 'B'; bytes[3] = 'B';
    put(bytes, 4, 1, 2); put(bytes, 6, 32, 2);
    put(bytes, 8, 16, 2); put(bytes, 10, 16, 2);
    put(bytes, 12, 1, 4); put(bytes, 16, 16667, 8);
    put(bytes, 32, 16667, 4); bytes[36] = static_cast<std::uint8_t>(codec);
    put(bytes, 38, palette, 2); put(bytes, 40, payload.size(), 4);
    put(bytes, 44, crc32_ieee(decoded.data(), decoded.size()), 4);
    bytes.insert(bytes.end(), payload.begin(), payload.end());
    seal(bytes);
    return bytes;
}

void rejects(const Bytes& bytes, AssetError expected) {
    AssetError error = AssetError::None;
    expect(!AssetReader::open(bytes.data(), bytes.size(), error), "malformed asset rejected");
    expect(error == expected, "malformed asset reports expected error");
}

void round_trip(const Bytes& bytes, const Bytes& decoded) {
    AssetError error = AssetError::BadFrame;
    auto reader = AssetReader::open(bytes.data(), bytes.size(), error);
    expect(reader.has_value() && error == AssetError::None, "valid asset opened");
    expect(reader->info().width == 16 && reader->info().height == 16 &&
           reader->info().frame_count == 1 && reader->info().duration_us == 16667,
           "header values read little-endian");
    std::array<Rgb8, 257> output{};
    output.back() = {17, 18, 19};
    auto result = reader->next(output.data(), 255);
    expect(result.error == AssetError::InsufficientOutput, "short output rejected");
    expect(output[0].red == 0, "short output does not write");
    result = reader->next(output.data(), 256);
    expect(result.status == DecodeStatus::Frame && result.frame_index == 0 && result.duration_us == 16667,
           "failed attempt does not advance cursor");
    for (std::size_t i = 0; i < 256; ++i) {
        expect(output[i].red == decoded[3*i] && output[i].green == decoded[3*i+1] &&
               output[i].blue == decoded[3*i+2], "every decoded channel matches");
    }
    expect(output.back().red == 17 && output.back().green == 18 && output.back().blue == 19,
           "output tail is untouched");
    expect(reader->next(nullptr, 0).status == DecodeStatus::End, "end is distinct from error");
    reader->rewind();
    expect(reader->next(output.data(), 256).frame_index == 0, "rewind restarts at first frame");
}
}  // namespace

int main() {
    constexpr std::uint8_t check[] = {'1','2','3','4','5','6','7','8','9'};
    expect(crc32_ieee(check, sizeof check) == 0xcbf43926U, "standard CRC golden vector");
    expect(crc32_ieee(nullptr, 0) == 0, "empty CRC");
    Bytes decoded;
    for (unsigned i = 0; i < 256; ++i) decoded.insert(decoded.end(), {1, 2, 3});
    const auto flat = asset(1, 0, {255, 1, 2, 3}, decoded);
    round_trip(flat, decoded);
    Bytes gradient;
    for (unsigned i = 0; i < 256; ++i) {
        gradient.insert(gradient.end(), {static_cast<std::uint8_t>(i),
                        static_cast<std::uint8_t>(255-i), static_cast<std::uint8_t>(i^85)});
    }
    const auto raw = asset(0, 0, gradient, gradient);
    round_trip(raw, gradient);
    Bytes palette_payload{1, 2, 3, 99, 100, 101}, alternating;
    for (unsigned i = 0; i < 256; ++i) {
        palette_payload.insert(palette_payload.end(), {0, static_cast<std::uint8_t>(i%2)});
        const auto offset = i%2 ? 3 : 0;
        alternating.insert(alternating.end(), palette_payload.begin()+offset, palette_payload.begin()+offset+3);
    }
    const auto palette = asset(2, 2, palette_payload, alternating);
    round_trip(palette, alternating);

    AssetError error;
    expect(!AssetReader::open(nullptr, 100, error) && error == AssetError::InvalidArgument, "null input rejected");
    expect(!AssetReader::open(flat.data(), kAssetMaxBytes+1, error) && error == AssetError::TooLarge,
           "oversize rejected before dereferencing alleged input span");
    for (std::size_t size = 0; size < flat.size(); ++size) {
        expect(!AssetReader::open(flat.data(), size, error) && error != AssetError::None,
               "every truncated prefix rejected");
    }
    auto mutation = flat; mutation[0] = 0; rejects(mutation, AssetError::BadMagic);
    mutation = flat; put(mutation, 4, 2, 2); rejects(mutation, AssetError::UnsupportedVersion);
    mutation = flat; put(mutation, 6, 33, 2); rejects(mutation, AssetError::BadHeader);
    mutation = flat; put(mutation, 8, 17, 2); rejects(mutation, AssetError::UnsupportedDimensions);
    mutation = flat; put(mutation, 12, 0, 4); rejects(mutation, AssetError::BadHeader);
    mutation = flat; put(mutation, 12, 0xffffffffU, 4); rejects(mutation, AssetError::ExpansionLimit);
    mutation = flat; put(mutation, 16, 1, 8); rejects(mutation, AssetError::DurationMismatch);
    mutation = flat; put(mutation, 24, 1, 4); rejects(mutation, AssetError::BadHeader);
    mutation = flat; mutation[28] ^= 1; rejects(mutation, AssetError::BadBodyChecksum);
    mutation = flat; put(mutation, 32, 0, 4); seal(mutation); rejects(mutation, AssetError::BadFrame);
    mutation = flat; mutation[36] = 255; seal(mutation); rejects(mutation, AssetError::BadFrame);
    mutation = flat; mutation[37] = 1; seal(mutation); rejects(mutation, AssetError::BadFrame);
    mutation = flat; put(mutation, 38, 1, 2); seal(mutation); rejects(mutation, AssetError::BadFrame);
    mutation = flat; put(mutation, 40, 0xffffffffU, 4); seal(mutation); rejects(mutation, AssetError::Truncated);
    mutation = flat; mutation[48] = 254; seal(mutation); rejects(mutation, AssetError::BadFrame);
    mutation = flat; mutation.insert(mutation.end(), {0, 1, 2, 3}); put(mutation, 40, 8, 4);
    seal(mutation); rejects(mutation, AssetError::BadFrame);
    mutation = flat; mutation.push_back(0); seal(mutation); rejects(mutation, AssetError::TrailingData);
    mutation = flat; put(mutation, 12, 2, 4); rejects(mutation, AssetError::Truncated);
    mutation = palette; mutation[55] = 2; seal(mutation); rejects(mutation, AssetError::BadFrame);
    mutation = palette; put(mutation, 38, 257, 2); seal(mutation); rejects(mutation, AssetError::BadFrame);
    mutation = palette; put(mutation, 38, 0, 2); seal(mutation); rejects(mutation, AssetError::BadFrame);
    mutation = raw; put(mutation, 40, 767, 4); seal(mutation); rejects(mutation, AssetError::BadFrame);

    auto reader = AssetReader::open(flat.data(), flat.size(), error);
    expect(reader->next(nullptr, 256).error == AssetError::InvalidArgument, "null output rejected");
    auto alias = flat;
    auto alias_reader = AssetReader::open(alias.data(), alias.size(), error);
    expect(alias_reader->next(reinterpret_cast<Rgb8*>(alias.data()), 256).error == AssetError::OverlappingOutput,
           "in-place decode rejected before writing");
    expect(alias == flat, "overlapping output leaves input unchanged");
    mutation = flat; mutation[44] ^= 1; seal(mutation);
    auto bad_crc = AssetReader::open(mutation.data(), mutation.size(), error);
    expect(bad_crc.has_value(), "decoded CRC is deferred until frame decode");
    std::array<Rgb8, 769> output{};
    output[256] = {17, 18, 19};
    const auto failed = bad_crc->next(output.data(), 256);
    expect(failed.error == AssetError::BadFrameChecksum && failed.frame_index == 0, "decoded corruption detected");
    for (unsigned i = 0; i < 256; ++i) expect(output[i].red == 0 && output[i].green == 0 && output[i].blue == 0,
                                            "bad-CRC output cleared to black");
    expect(output[256].red == 17, "bad-CRC clearing respects output boundary");
    expect(bad_crc->next(output.data(), 256).frame_index == 0, "failed checksum does not advance");

    // Native decoder output feeds the existing colour core without repacking.
    expect(reader->next(output.data(), 256).status == DecodeStatus::Frame, "pipeline frame decoded");
    const auto transform = ColorTransform::create(identity_gamma(), {65535,65535,65535}, 32768);
    const auto linear = transform->convert(output[0]);
    expect(linear.red == 129 && linear.green == 257 && linear.blue == 386, "decode-to-colour golden pixel");

    std::uint32_t random = 0x12345678;
    const std::array<Bytes, 3> fixtures{flat, raw, palette};
    for (unsigned trial = 0; trial < 4000; ++trial) {
        random ^= random << 13; random ^= random >> 17; random ^= random << 5;
        mutation = fixtures[trial%3];
        const auto position = random % mutation.size();
        mutation[position] ^= static_cast<std::uint8_t>(1U << ((random >> 16) % 8));
        if (position >= 32) seal(mutation);  // Reach structural checks past outer CRC.
        auto fuzz = AssetReader::open(mutation.data(), mutation.size(), error);
        if (fuzz) {
            output.back() = {17,18,19};
            const auto result = fuzz->next(output.data(), 768);
            expect(result.status == DecodeStatus::Frame || result.status == DecodeStatus::Error,
                   "mutated input yields a bounded result");
            expect(output.back().red == 17 && output.back().green == 18 && output.back().blue == 19,
                   "mutated input preserves output guard");
        } else {
            expect(error != AssetError::None, "mutated input failure has an error");
        }
    }
    std::cout << "Asset reader: " << checks << " checks passed\n";
}
