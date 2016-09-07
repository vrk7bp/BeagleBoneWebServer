# BeagleBoneWebServer
Step-By-Step instructions I used to make my BeagleBone at home into Web Server.

After getting frustrated with some crazy charges by Azure (I paid over $200 in a month to host my single page website), I decided to try to host
my own webserver using a BeagleBone Black that I purchased a couple of years ago. I wanted to track all the steps/hoops that I went through both
as a reference for me as well as a resource for other people who want to take the same route.

1) Updating the BeagleBone Black.

Its been about a year since I've even turned on my Beaglebone, so there are a couple of issues that I ran into. The most important ended up being
the fact that I lost the public certificates I needed to SSH into this Beaglebone. Once I upgraded my old PC to Windows 10, I also decided to clean
up a lot of programs since it was no longer going to be my main dev-machine. This purge included removing Putty, and the saved "login" to my Beaglebone.
So with this, I decided now would be a good time to update/clean flash my Beaglebone.

To do this, I used the 'Update Image' section from http://192.168.7.2/Support/BoneScript/updates/, which is the local server you can hit when your
BeagleBone is plugged in via USB. At a high-level, I...

	a) Downloaded the latest Debian image to my Windows PC
	b) Used 7-zip to decompress the file
	c) Grabbed a MicroSD Card and plugged into my PC using a MicroSD to SD Card converter
	d) Downloaded a program called Win32DiskImager to put this Debian Image on the MicroSD in a "bootable" format.
	e) Plugged MicroSD card in Beaglebone and rebooted it in "Boot" mode.

Key: Once your MicroSD card has been written to, make sure to edit the /boot/uEnv.txt file so that the '#' is removed from the 'cmdline=init=/opt/scripts/tools/eMMC/init-eMMC-flasher-v3.sh' line. 

2) Putting an Apache WebServer on the BeagleBone Black



