
* Obfuscating attacks using encodings
	* To take your skills further, you'll need to **adapt the techniques you've learned to overcome these additional obstacles**, unearthing vulnerabilities that other testers may have overlooked;
	* In this section, we'll provide some suggestions on how you **can obfuscate harmful payloads to evade input filters and other flawed defenses**. Specifically, you'll learn how to use standard encodings to take advantage of misconfigurations and handling discrepancies between connected systems.
*  Using [Burp Scanner](https://portswigger.net/burp/vulnerability-scanner) during manual testing
	* you can optimize your workflow by using Burp Scanner to supplement your own knowledge and intuition.
	* Not only does this reduce the chance of you overlooking things, it can save you valuable time by helping you to rapidly identify potential attack vectors;
	* This means you can concentrate your time and effort on things that can't be easily automated, such as working out how to exploit the vulnerable behavior or chain it with your other findings.

--- 

### Using Burp Scanner during manual testing

* Scanning a specific request
	* When you come across an interesting function or behavior, your first instinct may be to send the relevant requests to Repeater or Intruder and investigate further. **But it's often beneficial to hand the request to Burp Scanner as well**. It can get to work on the more repetitive aspects of testing while you put your skills to better use elsewhere;
	![[Pasted image 20230527112538.png]]
---

### Scanning custom insertion points

* Testing specific inputs
	* First, send the request to **Burp Intruder**. On the **Positions** tab, add payload positions to any insertion points you're interested in, then right-click and select **Scan defined insertion points**
	* You can then configure and launch a scan that will place payloads in these positions only. This lets you focus on the inputs you're interested in **rather than scanning a whole bunch of cookies that you know are unlikely to be of any use**
![[Pasted image 20230527115840.png]]
 * it's often quicker to use the [Scan manual insertion point](https://portswigger.net/bappstore/ca7ee4e746b54514a0ca5059329e926f) extension in this case. You can then highlight any sequence of characters within the request, typically a parameter value, and select **Extensions > Scan manual insertion point** from the context menu.
 * This approach can yield results incredibly quickly, giving you something to work with in just a couple of seconds. It also means you can choose to scan inputs that Burp Scanner normally doesn't use, such as custom header values.
---

### Scanning non-standard data structures

* As you're free to define insertion points in arbitrary positions, you can also target a specific substring within a value. Among other things, this can be useful for scanning non-standard data structures.
* Burp Scanner will treat this string `user=12312-carlos` as unique string. By manually defining an insertion point on each part of the value separately, you can accurately scan even non-standard data structures like this

![[Pasted image 20230527120847.png]]
