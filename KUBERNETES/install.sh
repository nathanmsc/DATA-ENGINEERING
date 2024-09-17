# Clear the terminal screen
sudo apt update
sudo apt upgrade -y
# Final message
clear
echo $USER > /home/$USER/username
sudo -i
su $(cat /home/$(ls /home)/username)
echo "DOCKER INSTALLATION COMPLETED SUCCESSFULLY"
