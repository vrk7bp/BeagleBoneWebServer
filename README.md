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

4) Setting a Static IP Address for the BeagleBone

Setting a static IP Address for your BeagleBone is (for most people) a two step process. Changes have to be made to both the BeagleBone and likely
your local router as well in order to get a static IP address supported.

First, on your BeagleBone, run the command `sudo nano /etc/network/interface`. This will allow you to edit the file that describes the network interfaces
that your system has. You must have root permissions to edit this file, hence the `sudo`. Next, we will focus on editing the `eth0` interface, which
is the ethernet connection on your board. If you want to edit a different interface (i.e. WiFi), then you can target other interfaces. Under any existing
interface definitions (represented by a code block with a line starting with `iface`), add the following:

```Linux
auto eth0
iface eth0 inet static
   address IP.Address.You.Want
   netmask 255.255.255.0
   gateway Router.LAN.IP.Address
```
Finally, restart your BeagleBone.

Lets breakdown this entry step-by-step. `auto eth0` is telling the system to start this interface when the system is booted up. `iface eth0 inet static`
is telling the system to configure interface eth0 (ethernet) with a static IP Address. `inet` is shorthand for internet. Since we are defining our own
IP Address here (hence `static`), the next line is denoting this address. `netmask` is always bundled with IP Addresses and denotes the part of the 
network on the LAN that this BeagleBone is a "part of" (or in other words, what other IP Addresses it can touch). Finally we come to `gateway` which
is essentially the place you're telling your BeagleBone to send packets with IP Addresses its not familiar with. Therefore, this should be your routers
LAN IP Address (which is usually `192.168.1.1`)

Now that you've made the necessary changes in the BeagleBone, chances are you're going to have to make some changes in your router too. It is highly
likely that your router is using the DHCP protocol to assign IP Addresses to your devices (DHCP at a high level is the way that your device gets a
new IP Address everytime it connects to the router). This will end up causing conflicts with your BeagleBone, so its better to manually add your
BeagleBone as a "special case".

Login to your router (this can be done in various ways depending on your router, but chances are typing `192.168.1.1` into your browser will bring you to the login
screen). You will usually find the DHCP settings under LAN. Once you hit your DHCP settings, you should have the option of setting some devices with
a manual configuration. This will require you to grab your BeagleBone's MAC Address (`ifconfig -a`, and look for the `eth0` interface, sometimes labeled
as HWAddress), and type the same static IP that you assigned above. 

Once these settings are propagated through your router, you should be good to go. In the same webpage for logging into your router, you should be
able to see your currently connected clients. You should be able to find your BeagleBone there with the IP Address you assigned. You may have to unplug
and replug your BeagleBone's ethernet/power before you see anything.

5) Connecting to the Rest of the Internet

We've now come to the final step. We will use a concept called Port Forwarding; at a high level, port forwarding is telling your router to re-route 
to a specific local IP Address when people access the router on a certain port. Given that we setup a static IP Address in the previous step, we
should now be able to port forward certain incoming calls to our BeagleBone. By default, the router acts as a Firewall preventing outside connections/requests
from entering into the local network. It isn't until we institute port forwarding that we "open up" the BeagleBone to the rest of the internet.

Instructions for setting up Port Forwarding on your router vary greatly, because of the hundreds of different producers and thousands of different models.
The easiest thing to do is Google "ROUTER MODEL port forwarding" and you should be able to find instructions to help you set things up. There are some
things to keep in mind:

	a) Choose the "Port Range" field wisely. The name might be different across routers, but this is the port that incoming calls are going to "connect to" in order to your BeagleBone server. Avoid "famous" ports such as 80 and 22.
	b) For the "Local Port" field, you'll want to put 80. This is because 80 is the port used for http, and the web server you have on your BeagleBone will default to this port. 
	c) Understand what you're doing. You are introducing a small hole in the previously solid router firewall. It may become possible for people to exploit this hole.

Once you apply these settings, you should be good to go! Grab your local IP Address (not the 192.168.YYY.YYY) which is represented by your routers
WAN IP Address. Otherwise you can just type into Google "what is my ip address" to find it. Then go into any brower and type in YOUR.LOCAL.IP.ADDRESS:PORT-RANGE-NUMBER.
And there you have it, now you have a fully functional web server!

Just to make my machine more robust, I also set-up port forwarding for SSH-ing into the BeagleBone as well. This means I added a new port forwarding
entry with a different "Port Range" and 22 as "Local Port".


And there you have it folks, pretty clear, step-by-step instructions on building your own server from a brand-new BeagleBone Black. I'll now begin
the process of porting my personal website from Azure to my local BeagleBone web server. I'll add a walkthrough below of that process, but probably
not as in-depth detail as I went into above.

A) Setting up a DDNS provider

Every once in a while, your external IP Address (the one that is "public facing") will be renewed by your ISP. There is never a clear time table of
when this happens, and this can get annoying as the host of a web-server or constant SSH-ing. In order to work around this, there is something called
DDNS (Dyncamic Domain Name Service) providers. These providers give you a "static" domain name that will be tied to your external IP Address. However,
what is cool is that these folks "re-adjust" this pointer whenever your external IP Address is updated, meaning that you never have to worry about
IP Addresses changing at bad times. Instead always use/reference the "static" domain name provided by your DDNS provider.

I personally recommend www.noip.com, as they have a free tier that sufficed for me, and were extremely easy to use. After you get a DDNS from them,
you will have to go to your router to set this up. Its worth noting that not all routers support DDNS, although most of the newer ones should. Setting
up DDNS on every router is different, and therefore a web search will be useful. My router had a really clear option for setting things up, and it
took less than 2 minutes (with 1 minute spent re-booting the router). 

B) Setting up a URL to point to your DDNS URL

Although it is easy to use the URL provided by the DDNS provider as your "go-to" URL, the one's provdied by the DDNS providers aren't always the "prettiest".
Instead, you may find it useful to purchase a URL from a DNS provider such as GoDaddy or Namecheap. Once you've purchased a nicer URL, it is easy to
configure this to point to your DDNS provided URL. I personally use Namecheap, so the instructions below are based on their UI, but the basics should
extend to all DNS providers. You are basically setting up two CNAME Records...

	1) Build one CNAME record based on your "root" host (this is represented by an '@' in Namecheap). For the host field, input an '@', and for the value, input your DDNS provided URL.
	2) Build another CNAME record for the "www" subroot host. For the host filed, input a 'www', and for the value, put in your Namecheap purchased URL.

And that's about it. After about 30 minutes, the amount of time it'll take for these records to propagate through, you should be able to type your purchased
URL and hit your BeagleBone Black server!

<b> Note: </b> This only works if the port-forwarding you setup in your router is for Port 80 (default port for http). These records don't allow entry
of other ports, so if you ended up setting up your port-forwading on your router (the one that your router is listening to, not port its forwarding
onto for the BBB) you'll have to change that before this'll work. 

C) Adding a larger partition to your MicroSD

As I was playing around with my BeagleBone early on, I started running into a "No space left on device" error. After some investigation, it looks like
the default partition for the MicroSD card if 4 GB, and since I'm bootin directly from the SDCard with a 4 GB image of the Debian OS, there isn't much
room left to do other things. Since I'm using a 16 GB MicroSD card, I figured I would expand the size of the partition in the hopes of fixing this error.

All the instructions that I followed can be found here: http://elinux.org/Beagleboard:Expanding_File_System_Partition_On_A_microSD. The instructions that I ran are:

	1) sudo su (Switch to Root User)
	2) fdisk /dev/mmcblk0 (Open fdisk program to manipulate SD Card partitions)
	3) 'p' (Look at current partitions)
	4) 'd' (Delete some partition, do this if you have more than one, deleting the second partition)
	5) 'n' (Make a new partition)
	6) 'p' (Make partition a primary partition)
	7) '2' (Make this the second parition)
	8) 'Enter' a couple of times for default settings (you can change the size of the parition here)
	9) 'w' (Write partitions to SD Card)
	10) 'sudo reboot' to restart BeagleBone
	11) 'sudo resize2fs /dev/mmcblk0p2' to have filesystem write to new parition

Sometimes after this process, the resize2fs command comes back with a "Bad Magic Number" error. One alternative is to go back to the fdisk tool, and
instead delete all paritions (1 and 2), and create a new partition with all the available space. After writing this to the disk and rebooting again,
you should be able to run the resize2fs command with no problem.

<b> Note: </b> I'm still in the process of figuring out the relationship between the 4 GB eMMC memory built into the BBB and the MicroSD card when
booting from the MicroSD card. It seems as if the 4 GB eMMC memory isn't being used at all, but this doesn't conceptually make sense to me. I'll increase
the partition size of the MicroSD card for now to fix my problem, and will investigate this further.

D) Resolving DNS Issues

It looks like somewhere down the road, my DNS configuration got screwed up. This showed up in weird ways, but the most telling was the fact my use of 
the `ping` command. Running `ping` with an IP Address (i.e. `ping 8.8.8.8`) worked fine while pinging with a URL did not (i.e. `ping google.com`). This
made it pretty clear that my DNS settings were off. 

This article proved to be very helpful for closing on my issues: https://wiki.debian.org/NetworkConfiguration#Defining_the_.28DNS.29_Nameservers.

At some point while I was going through this whole process, it looks like my resolv.conf file go out of whack. I had tried making physical changes
in the /etc/network/interfaces file that we played around with above, by adding a `nameservers 8.8.8.8` at the bottom of the eth0 interface description; but to no avail.
I ended up changing this to `nameservers ROUTER.LOCAL.IP.ADDRESS` and saved the file.

After some research, I found that Debian actually uses the resolv.conf file as the source of truth for DNS configuration. There is a program called
resolvconf that usually takes care of proper configuration of this file (meaning you shouldn't have to touch it since your changes will eventually
be overridden), but that wasn't working as well. What was funny was that I couldn't `sudo apt-get update resolvconf` since I couldn't resolve the URLs
that were used to grab the relevant files.

What I ended up doing was a two step process. I wasn't able to edit the existing resolv.conf file, so I deleted it (`sudo rm resolv.conf`) and created a
new one (`sudo nano resolv.conf`) with the following simple entry: `nameserver 192.168.1.1`. I also ran `chmod 644 resolv.conf` as a pre-caution, in 
order to ensure that all users had read permissions of the file. After this, I was able to `ping google.com` successfully. Even though this solved the problem, it was a little fragile.

In order to make this more resilient, I then went back and ran `sudo apt-get install resolvconf` in order to fix whatever was wrong before. After this
was installed correctly, I rebooted one more time. `resolvconf` rebuilds the resolv.conf file based on multiple "data points" and is able to deal with
multiple programs trying to reconfigure the DNS settings. One of these "data points" is the `/etc/network/interfaces file, where we already set the nameserver
as the local IP Address of the router (which has its own forwarding mechanisms to DNS servers). By rebooting, we allowed `resolvconf` to build the
`resolv.conf` file correctly.

Thanks for reading folks! Hopefully this proves to be useful for some folks down the road. And if there are any improvements/updates you guys find, just submit a pull request
and/or log an issue.
