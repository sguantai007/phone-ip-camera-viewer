import cv2
import configparser
from datetime import datetime
import time
from pathlib import Path
import requests

def load_camera_config():
    config = configparser.ConfigParser(interpolation=None)
    config.read('config.ini')

    camera_name = config['CAMERA']['name']
    camera_url = config['CAMERA']['url']

    return camera_name, camera_url


def check_camera_connection(camera_url):
    try:
        with requests.get(camera_url, stream=True, timeout=5) as response:
            response.raise_for_status()

            print('Camera is reachable')
            return True

    except requests.exceptions.Timeout:
        print('Camera connection timed out. Check that the camera is on.')

    except requests.exceptions.ConnectionError:
        print('Could not reach Camera. Check WiFi connection and camera.')

    except requests.exceptions.HTTPError:
        print('Camera return HTTP error, check the URL and credentials')

    except requests.exceptions.RequestException:
        print('Invalid camera URL or connection settings')

    return False



def reconnect_camera(camera_url, camera_name, max_attempts=3):
    for attempt in range(1, max_attempts + 1):
        print(f'Reconnection attempt {attempt}/{max_attempts}...')

        time.sleep(2)

        if not check_camera_connection(camera_url):
            continue

        new_camera = cv2.VideoCapture(camera_url, cv2.CAP_FFMPEG)

        if new_camera.isOpened():
            success, frame = new_camera.read()


            if success:
                print(f'Reconnected to {camera_name}')
                return new_camera

        new_camera.release()
        print('Could not receive a frame. Try again')

    print(f'Could not reconnect to {camera_name}')
    return None



def main():
    print('Program started')
    camera_name, camera_url = load_camera_config()
    print(f'Loaded camera: {camera_name}')

    if not check_camera_connection(camera_url):
        return

    camera = cv2.VideoCapture(camera_url, cv2.CAP_FFMPEG)
    print('Tried opening camera.')

    if not camera.isOpened():
        print(f'Could not connect to {camera_name}')
        camera.release()
        return

    print(f'Connected to {camera_name}. Press Esc to exit.')

    display_width = 960 

    previous_time = time.time()

    screenshot_dir = Path('screenshots')
    screenshot_dir.mkdir(exist_ok=True)

    recording_dir = Path('recordings')
    recording_dir.mkdir(exist_ok=True)

    video_writer = None
    recording = False
    recording_start_time = None

    try:
        while True:
            success, frame = camera.read()

            if not success:
                print('Camera connection lost. Attempting to reconnect...')

                camera.release()

                camera = reconnect_camera(camera_url, camera_name)

                if camera is None:
                    print('Unable to restore the camera connection.')
                    break

                previous_time = time.time()

                continue


            current_time = time.time()

            time_difference = current_time - previous_time

            if time_difference > 0:
                fps = 1/ time_difference
            else:
                fps = 0

            previous_time = current_time

            height, width = frame.shape[:2]

            display_height = int(height * display_width / width)

            frame = cv2.resize(frame, (display_width, display_height))

            timestamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

            cv2.putText(
                frame,
                timestamp,
                (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                camera_name,
                (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            resolution = f'Resolution: {width} x {height}'

            cv2.putText(
                frame,
                resolution,
                (10, 140),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            fps_text = f'FPS: {fps:.2f}'

            cv2.putText(
                frame,
                fps_text,
                (10, 180),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            if recording:
                video_writer.write(frame)

                elapsed_time = int(time.time() - recording_start_time)

                minutes = elapsed_time // 60
                seconds = elapsed_time % 60

                recording_text = f'REC {minutes:02d}:{seconds:02d}'

                cv2.putText(
                    frame,
                    recording_text,
                    (display_width - 200, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2
                )

            cv2.imshow(camera_name, frame)

            key = cv2.waitKey(1) & 0xFF

            if key == ord('r'):
                if not recording:
                    video_name = datetime.now().strftime(
                        'recording_%d%m%Y_%H%M%S.avi'
                    )

                    video_path = recording_dir / video_name

                    fourcc = cv2.VideoWriter_fourcc(*'XVID')

                    fps_value = 20.0

                    video_writer = cv2.VideoWriter(
                        str(video_path),
                        fourcc,
                        fps_value,
                        (display_width, display_height)
                    )

                    recording = True
                    recording_start_time = time.time()

                    print(f'Recording started: {video_path}')

                else:
                    recording = False

                    video_writer.release()
                    video_writer = None

                    recording_start_time = None

                    print(f'Recording saved: {video_path}')

            if key == ord('s'):
                screenshot_name = datetime.now().strftime(
                    'screenshot_%d%m%Y_%H%M%S.jpg'
                )

                screenshot_path = screenshot_dir / screenshot_name

                cv2.imwrite(str(screenshot_path), frame)

                print(f'Screenshot saved as {screenshot_path}')

            if key == 27:
                break

    except KeyboardInterrupt:
        print('Ctrl+C detected. Shutting down safely.')

    except Exception:
        print('An unexpected error occurred. Shutting down safely.')

    finally:
        if video_writer is not None:
            video_writer.release()
            print(f'Recording saved: {video_path}')

        if camera is not None:
            camera.release()

        cv2.destroyAllWindows()
        print('Camera released and windows closed.')


if __name__ == '__main__':
    main()




