import cv2
from tqdm import tqdm
import os


def video_to_frames(video_path, output_dir):
    """
    --- THIS FUNCTION WAS WRITTEN BY CHATGPT v3.5 ---

    Extract frames from a video, save them as image files, and write metadata to a file.

    Args:
        video_path (str): Path to the input video file.
        output_dir (str): Directory where frames will be saved.

    Returns:
        None
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Open the video file
    video_capture = cv2.VideoCapture(video_path)

    # Check if the video file was opened successfully
    if not video_capture.isOpened():
        raise ValueError("Error: Could not open video file.")

    # Get video properties
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

    # Write metadata to a text file
    metadata_file_path = os.path.join(output_dir, "metadata.txt")
    with open(metadata_file_path, "w") as metadata_file:
        metadata_file.write(f"Original Frame Rate: {fps} FPS\n")
        metadata_file.write(f"Total Frames: {total_frames}\n")

    # Loop through each frame and save it
    for frame_number in tqdm(range(total_frames), desc="Extracting Frames From Video"):
        # Read the next frame
        ret, frame = video_capture.read()

        # Check if the frame was read successfully
        if not ret:
            break

        # Save the frame as an image with a zero-padded filename
        frame_filename = os.path.join(output_dir, f"frame_{frame_number:05d}.png")
        cv2.imwrite(frame_filename, frame)

    # Release the video capture object and close the video file
    video_capture.release()


def frames_to_video(frames_dir, output_video_path):
    """
    --- THIS FUNCTION WAS WRITTEN BY CHATGPT v3.5 ---

    Convert frames in a specified directory to an MP4 video using metadata from the directory.

    Args:
        frames_dir (str): Directory containing the frames in "frame_%05d.png" format.
        output_video_path (str): Path to the output video file (e.g., "output_video.mp4").

    Returns:
        None
    """
    # Check if the frames directory exists
    if not os.path.exists(frames_dir):
        raise ValueError("Error: Frames directory does not exist.")

    # Check if metadata file exists in the frames directory
    metadata_file_path = os.path.join(frames_dir, "metadata.txt")
    if not os.path.exists(metadata_file_path):
        raise ValueError("Error: Metadata file not found in the frames directory.")

    # Read the frame rate from the metadata file
    with open(metadata_file_path, "r") as metadata_file:
        lines = metadata_file.readlines()
        for line in lines:
            if line.startswith("Original Frame Rate:"):
                fps = float(line.split(":")[1].strip().split()[0])
                break
        else:
            raise ValueError("Error: Metadata does not contain frame rate information.")

    # Get the list of frame files in the frames directory
    frame_files = [
        f
        for f in os.listdir(frames_dir)
        if f.startswith("frame_") and f.endswith(".png")
    ]
    frame_files.sort()

    # Determine the video frame size from the first frame
    first_frame = cv2.imread(os.path.join(frames_dir, frame_files[0]))
    frame_height, frame_width, _ = first_frame.shape

    # Initialize video writer
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video_writer = cv2.VideoWriter(
        output_video_path, fourcc, fps, (frame_width, frame_height)
    )

    # Write frames to the video with tqdm progress bar
    for frame_file in tqdm(frame_files, desc="Converting Frames To Video"):
        frame_path = os.path.join(frames_dir, frame_file)
        frame = cv2.imread(frame_path)
        video_writer.write(frame)

    # Release the video writer
    video_writer.release()
