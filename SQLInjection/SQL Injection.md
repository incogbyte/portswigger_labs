
### TL;DR

- SQL Injection cheat sheet
	- [https://portswigger.net/web-security/sql-injection/cheat-sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet)


![[Pasted image 20230529091416.png]]

### What is SQL Injection

- Web security vulnerability that allows an attacker to interfere with the queries that an application makes to its database.
- In some situations, an attacker can escalate a SQL injection attack to compromise the underlying server or other back-end infrastructure, or perform a denial-of-service attack.
### Impact of successful SQL Injection attack
- A successful SQL injection attack can result in unauthorized access to sensitive data.
- Reputational damage and regulatory fines.
- Leading to a long-term compromise that can go unnoticed for an extended period.

---

### How to detect SQL Injection vulnerabilities

- SQL injection can be detected manually by using a systematic set of tests against every entry point in the application. This typically involves
	- Submitting the single quote character `'` and looking for errors or other anomalies.
	- Submitting some SQL-specific syntax that evaluates to the base (original) value of the entry point, and to a different value, and looking for systematic differences in the resulting application responses.
	- Submitting Boolean conditions such as `OR 1=1` and `OR 1=2`, and looking for differences in the application's responses.
	- Submitting payloads designed to trigger time delays when executed within a SQL query, and looking for differences in the time taken to respond.
	- Submitting OAST payloads designed to trigger an out-of-band network interaction when executed within a SQL query, and monitoring for any resulting interactions.

--- 

### Blind SQL Injection vulnerabilities

- Blind SQL injection arises when an application is vulnerable to SQL injection, **but its HTTP responses do not contain the results of the relevant SQL query or the details of any database errors**.
- With blind SQL injection vulnerabilities, many techniques such as [`UNION` attacks](https://portswigger.net/web-security/sql-injection/union-attacks), **are not effective because they rely on being able to see the results of the injected query within the application's responses.**
- **Many instances of SQL injection are blind vulnerabilities** ( This means that the application does not return the results of the SQL query or the details of any database errors within its responses )
- Blind vulnerabilities can still be exploited to access unauthorized data, but the techniques involved are generally more complicated and difficult to perform.
- How to exploit blind vulnerabilities
	- You can change the logic of the query to trigger a detectable difference in the application's response depending on the truth of a single condition. This might involve injecting a new condition into some Boolean logic, or **conditionally triggering an error such as a divide-by-zero**.
	- You can conditionally trigger a time delay in the processing of the query, allowing you to infer the truth of the condition based on the time that the application takes to respond.
	- You can trigger an out-of-band network interaction, using [OAST](https://portswigger.net/burp/application-security-testing/oast) techniques. This technique is extremely powerful and works in situations where the other techniques do not. Often, you can directly exfiltrate data via the out-of-band channel, for example by placing the data into a DNS lookup for a domain that you control.
- Exploiting blind SQL Injection by triggering conditional responses
	- `…xyz' AND '1'='1 …xyz' AND '1'='2`
	- The first of these values will cause the query to return results, because the injected `AND '1'='1` condition is true. Whereas the second value will cause the query to not return any results, because the injected condition is false. This allows us to determine the answer to any single injected condition, and so extract data one bit at a time.
	- For example, suppose there is a table called `Users` with the columns `Username` and `Password`, and a user called `Administrator`. We can systematically determine the password for this user by sending a series of inputs to test the password one character at a time. To do this, we start with the following input:
	- ``xyz' AND SUBSTRING((SELECT Password FROM Users WHERE Username = 'Administrator'), 1, 1) > 'm``
	- This returns the "Welcome back" message, indicating that the injected condition is true, and so the first character of the password is greater than `m`.
	- Next, we send the following input: ``xyz' AND SUBSTRING((SELECT Password FROM Users WHERE Username = 'Administrator'), 1, 1) > 't` 
	- This does not return the "Welcome back" message, indicating that the injected condition is false, and so the first character of the password is not greater than `t`.
	- We can continue this process to systematically determine the full password for the `Administrator` user.
	- **The `SUBSTRING` function is called `SUBSTR` on some types of database.**

--- 

### Error-based SQL injection

- Error-based SQL injection refers to cases where you're able to use **error messages** to either extract or infer sensitive data from the database.
- You may be able to induce the application to return a specific error response based on the result of a boolean expression.
	- You can exploit this in the same way as the [conditional responses](https://portswigger.net/web-security/sql-injection/blind#exploiting-blind-sql-injection-by-triggering-conditional-responses) we looked at in the previous section.
	- You may be able to trigger error messages that output the data returned by the query. This effectively turns otherwise blind SQL injection vulnerabilities into "visible" ones. For more information, see [Extracting sensitive data via verbose SQL error messages](https://portswigger.net/web-security/sql-injection/blind#extracting-sensitive-data-via-verbose-sql-error-messages).
-  Exploiting blind SQL injection by triggering conditional errors
	-  it is often possible to induce the application to return conditional responses by triggering SQL errors conditionally, depending on an injected condition.
	- This involves modifying the query so that it will cause a database error if the condition is true, but not if the condition is false. Very often, an unhandled error thrown by the database will cause some difference in the application's response (such as an error message), allowing us to infer the truth of the injected condition.
	- To see how this works, suppose that two requests are sent containing the following `TrackingId` cookie values in turn:
```sql
xyz' AND (SELECT CASE WHEN (1=2) THEN 1/0 ELSE 'a' END)='a 
xyz' AND (SELECT CASE WHEN (1=1) THEN 1/0 ELSE 'a' END)='a
```
- These inputs use the `CASE` keyword to test a condition and return a different expression depending on whether the expression is true.
- With the first input, the `CASE` expression evaluates to `'a'`, which does not cause any error. With the second input, it evaluates to `1/0`, which causes a divide-by-zero error. Assuming the error causes some difference in the application's HTTP response, we can use this difference to infer whether the injected condition is true.
- Using this technique, we can retrieve data in the way already described, by systematically testing one character at a time:

```sql
`xyz' AND (SELECT CASE WHEN (Username = 'Administrator' AND SUBSTRING(Password, 1, 1) > 'm') THEN 1/0 ELSE 'a' END FROM Users)='a`
```

https://portswigger.net/web-security/sql-injection/blind
---

### SQL Injection Examples

- [Retrieving hidden data](https://portswigger.net/web-security/sql-injection#retrieving-hidden-data), where you can modify a SQL query to return additional results.
-  [Subverting application logic](https://portswigger.net/web-security/sql-injection#subverting-application-logic), where you can change a query to interfere with the application's logic.
-  [UNION attacks](https://portswigger.net/web-security/sql-injection/union-attacks), where you can retrieve data from different database tables.
- [Examining the database](https://portswigger.net/web-security/sql-injection/examining-the-database), where you can extract information about the version and structure of the database.
-  [Blind SQL injection](https://portswigger.net/web-security/sql-injection/blind), where the results of a query you control are not returned in the application's responses.