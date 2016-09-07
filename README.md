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

2) Setting up the BeagleBone Securely

Since we are essentially starting with a clean Debian OS image, its worth setting up a couple of things to make the BeagleBone more secure. The end
goal is to make this a Web Server to host my personal site (among other things), so therefore its probably worth adding some security measures to
make it hard to access. There are a couple of things that I did...

a) Setup a default user aside from Root

When the Debian image is first booted, all it has is a root user. This can be dangerous, since the root user has access to the entire system. In order
to make things a bit more secure, I created a default user using the adduser command. I also made sure to add this user to the "sudo" list so that
it is able to use the sudo command. This prevents me from having to login to the root user whenever I need to do more priviledged operations.

b) Setup different passwords for both users.

Using the passwd command, I set two different passwords for the two users. This way whenever someone tries to SSH into the server, they're required
to input the correct password. It is important to make sure that these passwords are different in order to ensure better protection.

c) Making sudo password the root password

By default, once the default user is added to the "sudo" list, the password that this user is required to input is its own. In other words, if the password
for the default user is compromised (as opposed to the root user), then this user essentially has root capabilities. Instead you can configure things
so that the root password is required to run a sudo command, as opposed to the default user's password. This is done by running the 'visudo' command
as the root user, and adding "Defaults rootpw" under the Defaults.


d) Add public-key SSH capabilities

Followed instructions at http://www.cyberciti.biz/faq/how-to-set-up-ssh-keys-on-linux-unix/. My understanding is that there are two things that you
can potentially do here. You can create a private key on your server, and share the public key out with any computers you may login from. It is highly
recommended that you add a Passphrase for the Public/Private Keys if you do this, as anyone with the Public Key (which can likely be easily compromised)
can login to your machine.

The other option is to follow the instructions on the page, and instead have the private key on the local machine you login to the server from and
have the server hold the public key. This means that the only way to login without the password is via a set of machines you already have setup with
this Public/Private relationship. As of now, this means that you can also try SSHing into the server with the users password, although there are
bound to be settings to change this.

Its definitely worth noting that I am far from a security expert. There is bound to be a load of other security measures that I should take in order
to prevent unauthorized access to this server. However these are the simple measures that I know off the top of my head. If any other suggestions pop-up
I'd be happy to research them/implement them on this Debian image.

3) Add Web Server to BeagleBone

After exploring a couple of tutorials, it looked like the lighttpd web server was the best option for my BeagleBone Black. Unlike Apache, lighttpd
is an asynchronous server, meaning that it is event-driven and handles requests with a limited amount of threads. Although my super simple server
is unlikely to hit massive loads, this asynchronous server tends to do better under high-load situations.

Given that we are dealing with a relatively "fresh" image of Debian, there are a couple of default services that are running on the BBB that we
have to disable. Disabling these services does two things for us; first it frees up memory and CPU cycles that may become critical under higher loads,
and second it frees up ports that are needed for the web server to run. The following commands should be run using a root account...

	a) systemctl disable cloud9.service
	b) systemctl disable gateone.service
	c) systemctl disable bonescript.service
	d) systemctl disable bonescript.socket
	e) systemctl disable bonescript-autorun.service
	f) systemctl disable avahi-daemon.service
	g) systemctl disable gdm.service
	h) systemctl disable mpd.service
	i) shutdown -r now (this command restarts the Beaglebone in order to activate the service disables)

After the BeagleBone is back on, you're ready to grab the lighttpd web-server. Simply run 'sudo apt-get install lighttpd' to get the web-server on
your BeagleBone. If you run '/var/www' you will find the default web-page for the server. Navigating to the IP Address of your BeagleBone (which you
can grab using 'ip addr show') in any broswer on your local network should navigate to this web page.

4) Dealing with the local IP Address


https://www.youtube.com/watch?annotation_id=ca149afa-f888-405d-a68b-2018ea38d8f1&feature=cards&src_vid=Vm-y-1HZSPo&v=uifOnB3ihKE


