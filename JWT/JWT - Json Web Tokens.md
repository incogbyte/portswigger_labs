
* JWT -> Json web tokens
	*  most commonly used in authentication, session management and access control

![img/Pasted image 20230523183126.png](img/Pasted image 20230523183126.png)

[img/Pasted image 20230523183126.png](img/Pasted image 20230523183126.png)

![[img/Pasted image 20230523183126.png]]

* What is JWT ?
	* JSON web tokens (JWTs) are a standardized format for sending cryptographically signed JSON data between systems.
	* They can contain any kind of data, but majority of times is used for access controle of users (session handler);
	* **JWT are stored in client-side A.K.A Browser**;
	* Are the common choice because of interection between servers;

* JWT Format
	* 3 Parts
		* header: **base64** part of the JWT (JSON Object)
		* Payload: **base64** part of the JWT (JSON Object)
		* Signature: Contains clains **claims** about the user
	 * In most cases, this data can be easily read or modified by anyone with access to the token. Therefore, the security of any JWT-based mechanism is **heavily reliant on the cryptographic signature**
	* Use the site [https://jwt.io/](https://jwt.io/) to decode the JWT or burp decoder function or bash;
	* JWT Example
	 ``` eyJraWQiOiI5MTM2ZGRiMy1jYjBhLTRhMTktYTA3ZS1lYWRmNWE0NGM4YjUiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTY0ODAzNzE2NCwibmFtZSI6IkNhcmxvcyBNb250b3lhIiwic3ViIjoiY2FybG9zIiwicm9sZSI6ImJsb2dfYXV0aG9yIiwiZW1haWwiOiJjYXJsb3NAY2FybG9zLW1vbnRveWEubmV0IiwiaWF0IjoxNTE2MjM5MDIyfQ.SYZBPIBg2CRjXAJ8vCER0LA_ENjII1JakvNQoP-Hw6GG1zfl4JyngsZReIfqRvIAEi5L4HV0q7_9qGhQZvy9ZdxEJbwTxRs_6Lb-fZTDpW6lKYNdMyjw45_alSCZ1fypsMWz_2mTpQzil0lOtps5Ei_z7mM7M8gCwe_AGpI53JxduQOaB5HkT5gVrv9cKu9CsW5MS6ZbqYXpGyOG5ehoxqm8DL5tFYaW3lB50ELxi0KsuTKEbD0t5BCl0aCR2MBJWAbN-xeLwEenaqBiwPVvKixYleeDQiBEIylFdNNIMviKRgXiYuAvMziVPbwSgkZVHeEdF5MQP1Oe2Spac-6IfA```

* Decoded JWT
![[Pasted image 20230523183914.png]]


* JWT Signature
	* The server that issues the token typically generates the signature by **hashing the header and payload** ( this can be encrypted ) this process need a  **sign key** to verify if the data inside the token was tampered. 
		* **Without knowing the server's secret signing key, it shouldn't be possible to generate the correct signature for a given header or payload.**

* JWT vs JWS vs JWE
	* The JWT spec is extended by both the JSON Web Signature (JWS) and JSON Web Encryption (JWE) specifications, which define concrete ways of actually implementing JWTs.
![[Pasted image 20230523184655.png]]

* JWT is a common JWS 
* JWE (E) are encrypted istead of encoding like JWS (JWT)

---

* Attacking JWT
	* Attack JWT usually tamper the JWT tokens to impersonate someone or broken the access control;
	* If an **attacker is able to create their own valid tokens with arbitrary values**, they may be able to escalate their own **privileges or impersonate other users**, taking full control of their accounts.
	* Flaws usually mean that **the signature of the JWT is not verified properly**;
	* If the server key is leaked in some way, or can be guessed or brute-forced, an attacker can generate a valid signature for any arbitrary token, compromising the entire mechanism;

* Exploiting JWT
	* By design, servers don't usually store any information about the JWTs that they issue;
	* The server doesn't actually know anything about the original contents of the token;

* Brute force the keys
	* Some signing algorithms, such as **HS256 (HMAC + SHA-256)**, use an arbitrary, standalone string as the secret key;
	* Just like a password, it's crucial that this secret **can't be easily guessed** or brute-forced by an attacker;
	* If the server uses an extremely weak secret, it may even be possible to brute-force this character-by-character rather than using a wordlist;
	* Wordlist to crack [https://raw.githubusercontent.com/wallarm/jwt-secrets/master/jwt.secrets.list](https://raw.githubusercontent.com/wallarm/jwt-secrets/master/jwt.secrets.list)
	* I'ts better to install hashcat [https://hashcat.net/hashcat/](https://hashcat.net/hashcat/)
		* Alternatives:
			* [https://github.com/ojensen5115/jwtcrack](https://github.com/ojensen5115/jwtcrack)
	* How to install [https://hashcat.net/wiki/doku.php?id=frequently_asked_questions#how_do_i_install_hashcat](https://hashcat.net/wiki/doku.php?id=frequently_asked_questions#how_do_i_install_hashcat)
	* Use the command bellow to run the hashcat with the wordlist
```bash
hashcat -a 0 -m 16500 <jwt> <wordlist>
```

* JWT Header parameter injections
	* According to the JWS specification, only the `alg` header parameter is mandatory. In practice, however, JWT headers (also known as JOSE headers) often contain several other parameters. **The following ones are of particular interest to attackers**
		* `jwk` (JSON Web Key) - Provides an embedded JSON object representing the key;
		*  `jku` (JSON Web Key Set URL) - Provides a URL from which servers can fetch a set of keys containing the correct key;
		* `kid` (Key ID) - Provides an ID that servers can use to identify the correct key in cases where there are multiple keys to choose from. Depending on the format of the key, this may have a matching `kid` parameter.

* Injecting self-signed JWTs via the jwk parameter
	* The JSON Web Signature (JWS) specification describes an optional `jwk` header parameter, which servers can use to **embed their public key directly within the token** itself in JWK format.
	* A JWK (JSON Web Key) is a standardized format for representing keys as a JSON object.
```json
{ 

"kid": "ed2Nf8sb-sD6ng0-scs5390g-fFD8sfxG", "typ": "JWT", "alg": "RS256", 
"jwk": { "kty": "RSA", "e": "AQAB", "kid": "ed2Nf8sb-sD6ng0-scs5390g-fFD8sfxG", "n": "yy1wpYmffgXBxhAUJzHHocCuJolwDqql75ZWuCQ_cb33K2vh9m" } }

```

* Ideally, servers should only use a **limited whitelist of public keys to verify JWT signatures**.However, misconfigured servers sometimes use any key that's embedded in the `jwk` parameter. You can exploit this behavior by signing a modified JWT **using your own RSA private key**, then embedding the matching public key in the `jwk` header
* How to do that, using burp:
	* With the extension loaded, in Burp's main tab bar, go to the **JWT Editor Keys** tab.
	* [Generate a new RSA key.](https://portswigger.net/burp/documentation/desktop/testing-workflow/session-management/jwts#adding-a-jwt-signing-key)
	* Send a request containing a JWT to Burp Repeater.
	* In the message editor, switch to the extension-generated **JSON Web Token** tab and [modify](https://portswigger.net/burp/documentation/desktop/testing-workflow/session-management/jwts#editing-jwts) the token's payload however you like.
	* Click **Attack**, then select **Embedded JWK**. When prompted, select your newly generated RSA key.
	* Send the request to test how the server responds.
	* **You can also perform this attack manually by adding the `jwk` header yourself. However, you may also need to update the JWT's `kid` header parameter to match the `kid` of the embedded key. The extension's built-in attack takes care of this step for you.**

* Injecting self-signed JWTs via the jku parameter
	* Instead of embedding public keys directly using the `jwk` header parameter, some servers let you use the `jku` (JWK Set URL) header parameter to reference a JWK Set containing the key. When verifying the signature, the server fetches the relevant key from this URL;
	* JWK Sets like this are sometimes exposed publicly via a standard endpoint, such as `/.well-known/jwks.json`.
	* More secure websites will only fetch keys from **trusted domains, but you can sometimes take advantage of URL parsing discrepancies to bypass this kind of filtering**
	* A JWK Set is a JSON object containing an array of JWKs representing different keys. You can see an example of this below

`{ "keys": [ { "kty": "RSA", "e": "AQAB", "kid": "75d0ef47-af89-47a9-9061-7c02a610d5ab", "n": "o-yy1wpYmffgXBxhAUJzHHocCuJolwDqql75ZWuCQ_cb33K2vh9mk6GPM9gNN4Y_qTVX67WhsN3JvaFYw-fhvsWQ" }, { "kty": "RSA", "e": "AQAB", "kid": "d8fDFo-fS9-faS14a9-ASf99sa-7c1Ad5abA", "n": "fc3f-yy1wpYmffgXBxhAUJzHql79gNNQ_cb33HocCuJolwDqmk6GPM4Y_qTVX67WhsN3JvaFYw-dfg6DH-asAScw" } ] }`

* Injecting self-signed JWTs via the kid parameter
	* Servers may use several cryptographic keys for signing different kinds of data, not just JWTs. For this reason, the header of a JWT may contain a `kid` (Key ID) parameter, which helps the server identify which key to use when verifying the signature;
	* **Verification keys are often stored as a JWK Set**. In this case, the server may simply look for the JWK **with the same `kid` as the token**. However, the JWS specification doesn't define a concrete structure for this ID - **it's just an arbitrary string of the developer's choosing**. For example, they might use the `kid` parameter to point to a particular entry in a database, or even the name of a file;
	* If this parameter is also vulnerable to [directory traversal](https://portswigger.net/web-security/file-path-traversal), an attacker could potentially force the server to use an arbitrary file from its filesystem as the verification key.
	  `{ "kid": "../../path/to/file", "typ": "JWT", "alg": "HS256", "k":`
	  ``
	  * This is especially dangerous if the server also supports JWTs signed using a [symmetric algorithm](https://portswigger.net/web-security/jwt/algorithm-confusion#symmetric-vs-asymmetric-algorithms). In this case, an attacker could potentially point the `kid` parameter to a predictable, static file, then sign the JWT using a secret that matches the contents of this file;
	  * You could theoretically do this with any file, but one of the simplest methods is to use `/dev/null`, which is present on most Linux systems. As this is an empty file, reading it returns an empty string. Therefore, signing the token with a empty string will result in a valid signature;
	  * **If you're using the JWT Editor extension, note that this doesn't let you sign tokens using an empty string. However, due to a bug in the extension, you can get around this by using a Base64-encoded null byte**

--- 

* Dealing with JWT with burpsuite
[[JWT/img/Pasted image 20230523185653.png]]
[[Pasted image 20230523185706.png]]
[[img/Pasted image 20230523185714.png]]



