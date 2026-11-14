// SPDX-License-Identifier: Apache-2.0
// Host utility: validates software asset integrity, not authenticity/hardware.
#include "rgb_badge/asset_reader.h"

#include <fstream>
#include <iostream>
#include <string>
#include <vector>

namespace {
const char* name(rgb_badge::AssetError error) {
    using rgb_badge::AssetError;
    switch(error) {
        case AssetError::None: return "none";
        case AssetError::InvalidArgument: return "invalid_argument";
        case AssetError::Truncated: return "truncated";
        case AssetError::TooLarge: return "too_large";
        case AssetError::BadMagic: return "bad_magic";
        case AssetError::UnsupportedVersion: return "unsupported_version";
        case AssetError::BadHeader: return "bad_header";
        case AssetError::UnsupportedDimensions: return "unsupported_dimensions";
        case AssetError::ExpansionLimit: return "expansion_limit";
        case AssetError::BadBodyChecksum: return "bad_body_checksum";
        case AssetError::BadFrame: return "bad_frame";
        case AssetError::BadFrameChecksum: return "bad_frame_checksum";
        case AssetError::InsufficientOutput: return "insufficient_output";
        case AssetError::OverlappingOutput: return "overlapping_output";
        case AssetError::DurationMismatch: return "duration_mismatch";
        case AssetError::TrailingData: return "trailing_data";
        case AssetError::MissingReference: return "missing_reference";
    }
    return "unknown";
}
} // namespace

int main(int argc,char** argv) {
    using namespace rgb_badge;
    if(argc==2 && std::string(argv[1])=="--help") {
        std::cout << "usage: rgbb-inspect FILE.rgbb\nValidate every RGBB frame and print a JSON summary.\n";
        return 0;
    }
    if(argc!=2) { std::cerr << "usage: rgbb-inspect FILE.rgbb\n"; return 2; }
    std::ifstream file(argv[1],std::ios::binary|std::ios::ate);
    if(!file || file.tellg()<0) { std::cerr << "Cannot read input file\n"; return 1; }
    if(file.tellg()>static_cast<std::streamoff>(kAssetMaxBytes)) {
        std::cerr << "Input exceeds the 16 MiB encoded asset limit\n"; return 1;
    }
    std::vector<std::uint8_t> bytes(static_cast<std::size_t>(file.tellg()));
    file.seekg(0);
    if(!file.read(reinterpret_cast<char*>(bytes.data()),static_cast<std::streamsize>(bytes.size())) ||
       file.peek()!=std::ifstream::traits_type::eof() || file.bad()) {
        std::cerr << "Input read failed or file size changed\n"; return 1;
    }
    AssetError error;
    auto reader=AssetReader::open(bytes.data(),bytes.size(),error);
    if(!reader) { std::cerr << "Invalid asset: " << name(error) << '\n'; return 1; }
    std::array<Rgb8,768> pixels{};
    std::uint32_t decoded_frames=0;
    for(;;) {
        const auto result=reader->next(pixels.data(),pixels.size());
        if(result.status==DecodeStatus::End) break;
        if(result.status==DecodeStatus::Error) {
            std::cerr << "Invalid frame " << result.frame_index << ": " << name(result.error) << '\n';
            return 1;
        }
        ++decoded_frames;
    }
    const auto& info=reader->info();
    const auto decoded_bytes=std::uint64_t{info.width}*info.height*decoded_frames*3;
    // Emit no success summary until every decoded frame has passed its CRC.
    std::cout << "{\"format\":\"RGBB\",\"version\":" << info.version
              << ",\"width\":" << info.width << ",\"height\":" << info.height
              << ",\"frame_count\":" << decoded_frames << ",\"duration_us\":" << info.duration_us
              << ",\"encoded_bytes\":" << bytes.size() << ",\"decoded_rgb888_bytes\":" << decoded_bytes
              << ",\"all_frame_checksums_valid\":true}\n";
    if(!std::cout) { std::cerr << "Summary output failed\n"; return 1; }
}
