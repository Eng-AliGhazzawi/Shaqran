import subprocess
import re
import argparse

def extract_last_stream(heic_file, ffmpeg_executable):
    # Use ffmpeg to get stream information
    result = subprocess.run([ffmpeg_executable, "-i", heic_file], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    output = result.stderr.decode('utf-8')

    # Regular expression to match stream IDs
    stream_pattern = re.compile(r'Stream #0:(\\d+)')

    # Extract all stream IDs
    stream_ids = stream_pattern.findall(output)
    print(f"Found streams: {stream_ids}")

    # Extract the last stream (assuming it's the depth map)
    last_stream_id = stream_ids[-1]
    depth_map_output = heic_file.replace('.HEIC', '_depth_map.png')

    # Extract the stream
    subprocess.run([ffmpeg_executable, "-i", heic_file, "-map", f"0:{last_stream_id}", depth_map_output])

    print(f"Depth map extracted and saved as '{depth_map_output}'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract the last stream from a HEIC file (typically the depth map).")
    parser.add_argument('--ffmpeg_path', required=True, help='Path to the ffmpeg executable.')
    parser.add_argument('--heic_file_path', required=True, help='Path to the HEIC file.')
    args = parser.parse_args()
    extract_last_stream(args.heic_file_path, args.ffmpeg_path)
