
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


--- 

### Obfuscating attacks using encodings

*  Context-specific decoding
	* Both clients and servers use a variety of different encodings to pass data between systems.
	* When they want to actually use the data, this often means they have to decode it first
	* When constructing an attack, you should think about where exactly your payload is being injected
	* If you can infer how your input is being decoded based on this context, you can potentially identify alternative ways to represent the same payload
* Decoding discrepancies
	* Injection attacks often involve injecting payloads that use recognizable patterns, such as HTML tags, JavaScript functions, or SQL statements.
	*  websites often implement defences that block requests containing these suspicious patterns.
	* However, these kinds of **input filters** also need **to decode the input in order to check whether it's safe or not**
	* It's vital that the decoding performed when checking the input is the same as the decoding performed by the back-end server or browser when it eventually uses the data.
* Obfuscation via URL encoding
	* In URLs, a series of reserved characters carry special meaning Ex:
		* `&` ->  separate parameters
		* = -> receive a value
		* ?parameter= -> this a full parameter
	* **Browsers automatically URL encode any characters that may cause ambiguity for parsers**. This usually means substituting them with a `%` character and their 2-digit hex code as follows:
		* `[...]/?search=Fish+%26+Chips`
	 * **Any URL-based input is automatically URL decoded server-side** before it is assigned to the relevant variables
	* Sequences like `%22`, `%3C`, and `%3E` in a query parameter are synonymous with `"`, `<`, and `>` characters respectively. ( you can inject URL-encoded data via the URL and it will usually still be interpreted correctly by the back-end application ).
	* Smuggle payloads to the back-end application simply by encoding any characters or words that are blacklisted, example:
		*  For example, in a SQL injection attack, you might encode the keywords, so `SELECT` becomes `%53%45%4C%45%43%54` and so on.
*  Obfuscation via double URL encoding
	*  Some servers perform **two rounds of URL decoding** on any URLs they receive.
	* This discrepancy enables an attacker to smuggle malicious input to the back-end by simply encoding it twice.
	* If you are blocked using the URL encode payload ``[...]/?search=%3Cimg%20src%3Dx%20onerror%3Dalert(1)%3E`` try to double encode using %25 for each `%` character. Example: ``[...]/?search=%253Cimg%2520src%253Dx%2520onerror%253Dalert(1)%253E`` . As the WAF only decodes this once, **it may not be able to identify that the request is dangerous. If the back-end server subsequently double-decodes** this input, the payload will be successfully injected
* Obfuscation via HTML encoding
	* In HTML documents, certain characters **need to be escaped or encoded** to prevent the browser from incorrectly interpreting them as part of the markup.
	* This is achieved by substituting the offending characters with a reference, prefixed with an ampersand and terminated with a semicolon.
	* This is achieved by substituting the offending characters with a reference, prefixed with an ampersand and terminated with a semicolon, example `&colon`; or can be a hexadecimal or decimal number: `&#58;` `&#x3a;` 
	* Browsers will automatically decode these  references (ampersand references)  when they parse the document;
	* You can occasionally take advantage of this to **obfuscate payloads for client-side attack**.
	*  If the server-side checks are looking for the `alert()` payload explicitly, they might not spot this if you HTML encode one or more of the characters: `<img src=x onerror="&#x61;lert(1)">` ( When the browser renders the page, it will decode and execute the injected payload. )
* Leading Zeros

--- 

