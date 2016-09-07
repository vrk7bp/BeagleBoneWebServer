# BeagleBoneWebServer
Step-By-Step instructions I used to make my BeagleBone at home into Web Server.

After getting frustrated with some crazy charges by Azure (I paid over $200 in a month to host my single page website), I decided to try to host
my own webserver using a BeagleBone Black that I purchased a couple of years ago. I wanted to track all the steps/hoops that I went through both
as a reference for me as well as a resource for other people who want to take the same route.

These instructions are for an Element14 BeagleBone Black Rev C. These instructions should be the same for a non Element14 BBB Rev C as well.

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
	e) Plugged MicroSD card in Beaglebone and rebooted it (by unplugging it and plugging it back in)

Note: As of early 2016, the https://beagleboard.org/latest-images site changed. Before, you would have the option to download an eMMC version or a
non-eMMC version to the microSD card. The eMMC version would write to the internal memory of the board, while the non-eMMC version will boot directly
from the memory card. As you can guess, this means that the non-eMMC version would require the microSD card to be plugged in at all times (since
the OS is booting directly from the card). This is likely less ideal for most folks, as the eMMC version allows you to use the same microSD card to
flash the OS across multiple boards.

Now, the https://beagleboard.org/latest-images site only allows you to download one type of image. By default this is the non-eMMC version. In order
to make this the eMMC version, you have to edit the /boot/uEnv.txt file on the Linux partition on the microSD card and remove the '#' on the line 
with 'cmdline=init=/opt/scripts/tools/eMMC/init-eMMC-flasher-v3.sh'. This will also require you to slightly alter step e above, instead powering
the BBB in "boot" mode by pressing the "User Boot" button near the microSD slot while inputting power.

For some reason, I wasn't able to get the eMMC version working properly for my BBB, so I decided to go with the non-eMMC version moving forward (with
the hope of coming back later and figuring out what was wrong). There are a couple of red flags that I found that I think may cause the error:

	a) Multiple sources said that writing to the eMMC would require at least 5 V of power, something that mini USB can't provide. You would need a separate power source in order to correctly write to the eMMC.
	b) Writing to the uEnv.txt file proved to be tough. I had to do this from a Linux machine as Windows couldn't recognize the file format of the microSD card after writing the Debian image to it. For some reason after editing the file, it seemed like the microSD card would become corrupt.

After playing around for a little while, I figured it would be easier to simply move forward booting from the microSD card.

2) Putting an Apache WebServer on the BeagleBone Black



