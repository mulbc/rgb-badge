// SPDX-License-Identifier: Apache-2.0
// Host-only trace adapter for compiler/playback integration tests.
#include "rgb_badge/asset_playback.h"

#include <charconv>
#include <fstream>
#include <iostream>
#include <iterator>
#include <limits>
#include <string>
#include <vector>

namespace {
bool number(const std::string& text, std::uint64_t& value) {
    const auto parsed=std::from_chars(text.data(),text.data()+text.size(),value);
    return parsed.ec==std::errc{} && parsed.ptr==text.data()+text.size();
}
void emit(const rgb_badge::AssetPlayback& p, const rgb_badge::PlaybackResult& r) {
    std::cout << "{\"status\":" << static_cast<unsigned>(r.status)
              << ",\"error\":" << static_cast<unsigned>(r.error)
              << ",\"asset_error\":" << static_cast<unsigned>(r.asset_error)
              << ",\"frame_index\":" << r.frame_index << ",\"duration_us\":" << r.duration_us
              << ",\"scheduled_start_us\":" << r.scheduled_start_us
              << ",\"scheduled_end_us\":" << r.scheduled_end_us
              << ",\"lateness_us\":" << r.lateness_us << ",\"rgb888\":\"";
    constexpr char hex[]="0123456789abcdef";
    for (std::size_t i=0; i<p.pixel_count(); ++i) {
        const auto pixel=p.pixels()[i];
        for (auto channel : {pixel.red,pixel.green,pixel.blue}) std::cout << hex[channel>>4] << hex[channel&15];
    }
    std::cout << "\"}\n";
}
} // namespace
int main(int argc, char** argv) {
    std::uint64_t budget=0, start=0;
    if (argc!=4 || !number(argv[2],budget) || budget>std::numeric_limits<std::uint32_t>::max() || !number(argv[3],start)) return 2;
    std::ifstream input(argv[1],std::ios::binary);
    if (!input) return 2;
    const std::vector<std::uint8_t> bytes((std::istreambuf_iterator<char>(input)),{});
    rgb_badge::AssetError error;
    auto reader=rgb_badge::AssetReader::open(bytes.data(),bytes.size(),error);
    if (!reader) { std::cerr << "open error " << static_cast<unsigned>(error) << '\n'; return 1; }
    rgb_badge::AssetPlayback player(*reader,static_cast<std::uint32_t>(budget));
    emit(player,player.start(start));
    std::string timestamp;
    while (std::cin>>timestamp) {
        std::uint64_t now=0;
        if (!number(timestamp,now)) return 2;
        emit(player,player.poll(now));
    }
    return 0;
}
