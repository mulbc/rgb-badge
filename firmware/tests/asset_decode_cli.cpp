// SPDX-License-Identifier: Apache-2.0
// Host integration adapter; not target firmware or a flash-writing utility.
#include "rgb_badge/asset_reader.h"

#include <fstream>
#include <iostream>
#include <vector>

int main(int argc, char** argv) {
    using namespace rgb_badge;
    if (argc != 2) { std::cerr << "usage: asset_decode FILE\n"; return 2; }
    std::ifstream file(argv[1], std::ios::binary | std::ios::ate);
    if (!file || file.tellg() < 0 || file.tellg() > static_cast<std::streamoff>(kAssetMaxBytes)) {
        std::cerr << "invalid input file\n"; return 1;
    }
    std::vector<std::uint8_t> bytes(static_cast<std::size_t>(file.tellg()));
    file.seekg(0);
    if (!file.read(reinterpret_cast<char*>(bytes.data()), static_cast<std::streamsize>(bytes.size()))) {
        std::cerr << "input read failed\n"; return 1;
    }
    AssetError error;
    auto reader = AssetReader::open(bytes.data(), bytes.size(), error);
    if (!reader) { std::cerr << "asset open error " << static_cast<unsigned>(error) << '\n'; return 1; }
    std::array<Rgb8, 768> output{};
    std::vector<std::uint32_t> durations;
    for (;;) {
        const auto frame = reader->next(output.data(), output.size());
        if (frame.status == DecodeStatus::End) break;
        if (frame.status == DecodeStatus::Error) {
            std::cerr << "asset frame error " << static_cast<unsigned>(frame.error) << '\n'; return 1;
        }
        durations.push_back(frame.duration_us);
        const std::size_t pixels = reader->info().width * reader->info().height;
        for (std::size_t i = 0; i < pixels; ++i) {
            const char rgb[]{static_cast<char>(output[i].red), static_cast<char>(output[i].green),
                             static_cast<char>(output[i].blue)};
            std::cout.write(rgb, sizeof rgb);
        }
    }
    if (!std::cout) { std::cerr << "output write failed\n"; return 1; }
    std::cerr << "{\"version\":" << reader->info().version
              << ",\"width\":" << reader->info().width << ",\"height\":" << reader->info().height
              << ",\"duration_us\":" << reader->info().duration_us << ",\"durations_us\":[";
    for (std::size_t i = 0; i < durations.size(); ++i) {
        if (i) std::cerr << ',';
        std::cerr << durations[i];
    }
    std::cerr << "]}\n";
}
