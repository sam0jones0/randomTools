#! python3
# ffmpegAudioDouble.py - Increases volume of all .mkv files in CWD by 250% using ffmpeg
# running in 2 threads
# ffmpeg.exe must be in PATH

import os
import send2trash
import threading

# Function takes list of episodes to run ffmpeg command with
def increaseVolume(splitList):
    for episode in splitList:
        os.system(f'ffmpeg.exe -i {episode} -c:v copy -af "volume=2.5" {episode}_output.mkv')
        send2trash.send2trash(episode)
        os.rename(f'{episode}_output.mkv', episode)

# Create list of episodes in current folder
episodeList = []
for filename in os.listdir('.'):
    if not filename.endswith('.mkv'):
        continue # Skip non .mkv files
    episodeList.append(filename)

workerThreads = []
for i in range (0, 2):
    # Split list of episodes in half
    if i == 0:
        splitList = episodeList[:len(episodeList) // 2]
    else:
        splitList = episodeList[len(episodeList) // 2:]
    # Start thread for each list of half the episodes
    workerThread = threading.Thread(target=increaseVolume, args=(splitList,))
    workerThreads.append(workerThread)
    workerThread.start()

# Wait for all threads to end
for workerThread in workerThreads:
    workerThread.join()

print('Done')

