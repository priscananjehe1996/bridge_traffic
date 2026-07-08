import time
import os
import subprocess

print("Waiting for photos copy to finish...")

while True:
    # check if the task is still running by checking if the copy_photos.py process is alive
    # A simpler way is to check the number of photos, but since we don't know the exact final number, 
    # we can check if it hasn't changed for 2 minutes.
    
    count1 = len(os.listdir('d:/OneDrive/Bridge stuff/bridge_traffic_deploy/PHOTOS'))
    time.sleep(60)
    count2 = len(os.listdir('d:/OneDrive/Bridge stuff/bridge_traffic_deploy/PHOTOS'))
    
    if count1 == count2 and count1 > 100:
        print("Copy seems to have finished!")
        break

print("Adding to git...")
subprocess.run(['git', 'add', '.'], cwd='d:/OneDrive/Bridge stuff/bridge_traffic_deploy')
print("Committing to git...")
subprocess.run(['git', 'commit', '-m', 'Add 50 charts, fix region unknowns, copy photos to local, add summary tables'], cwd='d:/OneDrive/Bridge stuff/bridge_traffic_deploy')
print("Pushing to git...")
subprocess.run(['git', 'push'], cwd='d:/OneDrive/Bridge stuff/bridge_traffic_deploy')
print("Done!")
